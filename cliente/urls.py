from django.conf.urls import patterns, url

from cliente.views import FacturaPDF

urlpatterns = patterns('cliente.views',
                       url(r'factura_pdf/(?P<pedido_id>[-_:\w\d]+)', FacturaPDF.as_view(), name='factura_pdf'),
                       )
