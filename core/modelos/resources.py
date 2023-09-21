from import_export import resources, fields, widgets
from .pedidos import Pedido
from .producto import Producto
from import_export.widgets import ManyToManyWidget
from import_export.fields import Field
from django.db.models.fields.related import ForeignKey
        
class ProductoResource(resources.ModelResource):
    class Meta:
        model = Producto
        
#-------Widget Modificados para poblar tabla intermedia---------#

class AssocManyToManyWidget(widgets.ManyToManyWidget):
    """
            nomenclature throughout class:
                model - or "m", target model of this relationship
                assoc - or "a", model through which relationship is implemented
                src - or "s" the model this field belongs to
    """
    SEP_DICT = dict(inst=',', main=':', val='=', asn='|')

    def __init__(self, relation, sep=None, assoc_fields=None, model_fields=None, *args, **kwargs):
        """
        :param relation: the ManyToManyRelation
        :param sep: a dict of separators to render/parse the field

        example output string:
        model_field1=z1|model_field2=w1:assoc_field1=x1,model_field1=z2|model_field2=w2:assoc_field1=x2,...
        """
        super(AssocManyToManyWidget, self).__init__(*args, **kwargs)

        a_fields = assoc_fields or [f.name for f in relation.through._meta.fields
                                    if not f.auto_created and not isinstance(f, ForeignKey)]

        self.with_assoc = len(a_fields) > 0
        if not self.with_assoc: return # if there are no association objects, default to regular ManyToManyWidget
        if sep is None: sep = AssocManyToManyWidget.SEP_DICT
        self.sep = sep

        self.assoc = relation.through
        self.source = relation.related_model
        # collect all fields that will be exported
        self.m_fields = model_fields or ['pk']
        self.a_fields = a_fields

        # collect names of reference fields
        fk_field = lambda src, dst: next(f for f in src._meta.fields
                                         if isinstance(f, ForeignKey) and f.related_model == dst)
        a2s_field = fk_field(self.assoc, self.source)
        self.a2s, self.s2a = a2s_field.name, a2s_field.remote_field.name
        a2m_field = fk_field(self.assoc, self.model)
        self.a2m, self.m2a = a2m_field.name, a2m_field.remote_field.name

    def render(self, value, obj=None):
        f = self._render if self.with_assoc else super().render
        return f(value, obj)

    def clean(self, value, row=None, *args, **kwargs):
        f = self._clean if self.with_assoc else super().clean
        return f(value, row, *args, **kwargs)

    def format_fv(self, field, instance):
        return '%s%s%s' % (field, self.sep['val'], str(getattr(instance, field)))

    def _render(self, value, obj=None):
        s = []
        for assoc in getattr(obj, self.s2a).all():
            afields = self.sep['asn'].join(self.format_fv(f, assoc) for f in self.a_fields)
            model = getattr(assoc, self.a2m)
            mfields = self.sep['asn'].join(self.format_fv(f, model) for f in self.m_fields)
            s.append(self.sep['main'].join([mfields, afields]))
        return self.sep['inst'].join(s)

    def fieldvalues_dict(self, fvs):  # does not maintain order?
        return dict(fv.split(self.sep['val']) for fv in fvs.split(self.sep['asn']))

    def _clean(self, value, row=None, *args, **kwargs):
        assoc_attrs = []
        for instance_str in value.split(self.sep['inst']):
            mfields, attr = [self.fieldvalues_dict(x) for x in instance_str.split(self.sep['main'])]
            attr.update({self.a2m: self.model.objects.get(**mfields)})
            assoc_attrs.append(attr)
        return assoc_attrs


class FKWidget(widgets.ForeignKeyWidget):
    """
            nomenclature throughout class:
                model - or "m", target model of this relationship
                assoc - or "a", model through which relationship is implemented
                src - or "s" the model this field belongs to
    """
    SEP_DICT = dict(val='=', field=',')

    def __init__(self, sep=None, model_fields=None, *args, **kwargs):
        """
        :param relation: the ManyToManyRelation
        :param sep: a dict of separators to render/parse the field

        example output string:
        model_field1=z1|model_field2=w1:assoc_field1=x1,model_field1=z2|model_field2=w2:assoc_field1=x2,...
        """
        super(FKWidget, self).__init__(*args, **kwargs)
        if sep is None: sep = FKWidget.SEP_DICT
        self.sep = sep
        self.m_fields = model_fields or ['pk']

    def render(self, value, obj=None):
        return self.sep['field'].join([self.format_fv(x, value) for x in self.m_fields])

    def clean(self, value, row=None, *args, **kwargs):
        return self.model.objects.get(**self.fieldvalues_dict(value))

    def format_fv(self, field, instance):
        return '%s%s%s' % (field, self.sep['val'], str(getattr(instance, field)))

    def fieldvalues_dict(self, fvs):  # does not maintain order?
        return dict(fv.split(self.sep['val']) for fv in fvs.split(self.sep['field']))


class AssocField(fields.Field):

    def save(self, obj, data, is_m2m):
        """
        Cleans this field value and assign it to provided object.
        """
        if not self.readonly:
            if self.widget.with_assoc:
                self.widget.assoc.objects.filter(**{self.widget.a2s: obj}).delete()  # delete old associations of this object
                for assoc_dict in self.clean(data):
                    assoc_dict[self.widget.a2s] = obj
                    self.widget.assoc.objects.create(**assoc_dict)
            else:
                getattr(obj, self.attribute).set(self.clean(data))

    def export(self, obj):
        """
        Returns value from the provided object converted to export
        representation.
        """
        value = self.get_value(obj)
        return "" if value is None else self.widget.render(value, obj)


class ModelResource(resources.ModelResource):
    @classmethod
    def field_from_django_field(cls, field_name, django_field, readonly):
        """
        Returns a Resource Field instance for the given Django model field.

        In case of a m2m field return the AssocField with an AssocManyToManyWidget instead of regular defaults
        """
        if django_field.get_internal_type() in ('ManyToManyField',):
            Field = AssocField
            FieldWidget = AssocManyToManyWidget
            widget_kwargs = dict(model=django_field.remote_field.model,
                                 relation=django_field.remote_field)
        elif django_field.get_internal_type() in ('ForeignKey',):
            Field = fields.Field
            FieldWidget = FKWidget
            widget_kwargs = dict(model=django_field.remote_field.model)
        else:
            Field = cls.DEFAULT_RESOURCE_FIELD
            FieldWidget = cls.widget_from_django_field(django_field)
            widget_kwargs = cls.widget_kwargs_for_field(field_name)

        return Field(attribute=field_name,
                     column_name=field_name,
                     widget=FieldWidget(**widget_kwargs),
                     readonly=readonly,
                     default=django_field.default)
    
 #-------Fin Widget Modificados para poblar tabla intermedia---------#   

#-------------------------------Inicio Resources-------------------------------#
#Resource para Pedidos

class PedidoResource(ModelResource):

    producto = AssocField(column_name='producto',attribute='producto',
                widget=AssocManyToManyWidget(model=Producto, relation=Pedido._meta.get_field('producto').remote_field,  # Provide both model and relation
                                            model_fields=['nombre'], separator='|'))
    class Meta:
        model = Pedido
        fields = ('id', 'cliente', 'fecha_produccion','fecha_entrega', 'orden_pedido', 'comentario', 'nombre', 'producto', 'prioridad','version', 'estado')
      #  export_order = ('id', 'cliente', 'fecha_produccion','fecha_entrega', 'orden_pedido', 'comentario', 'nombre', 'producto', 'prioridad','version', 'estado')

