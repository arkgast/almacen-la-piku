from easy_pdf.views import PDFTemplateView
from django.shortcuts import render_to_response

from cliente.models import PedidoCliente, DetallePedidoCliente


class FacturaPDF(PDFTemplateView):
    template_name = "factura_pdf.html"

    def get_context_data(self, **kwargs):
        encrypted_id = kwargs['pedido_id']
        pedido_id = PedidoCliente.decryptId(encrypted_id)
        pedido = PedidoCliente.objects.get(pk=pedido_id)
        detalle_pedido = DetallePedidoCliente.objects.filter(pedido=pedido)
        kwargs['pedido'] = pedido
        kwargs['detalle_pedido'] = detalle_pedido
        return super(FacturaPDF, self).get_context_data(
            page_size="A4",
            title="Factura",
            **kwargs
        )


def test_view(request):
    return render_to_response('test.html', {})
