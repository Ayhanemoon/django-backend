from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from shop.payments.models import Payment
from .serializers import PaymentSerializer


class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Payment API (read + simulate gateway actions).

    - Users can view their payments
    - Success/failure is simulated via actions
    """

    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(
            order__profile=self.request.user.profile
        )

    @action(detail=True, methods=["post"])
    def success(self, request, pk=None):
        """
        Simulate successful payment (gateway callback).
        """
        payment = self.get_object()

        if payment.status != payment.Status.PENDING:
            return Response(
                {"detail": "Payment already processed."},
                status=400,
            )

        payment.mark_success()

        return Response({
            "detail": "Payment marked as SUCCESS.",
            "order_status": payment.order.status,
        })

    @action(detail=True, methods=["post"])
    def fail(self, request, pk=None):
        """
        Simulate failed payment (gateway callback).
        """
        payment = self.get_object()

        if payment.status != payment.Status.PENDING:
            return Response(
                {"detail": "Payment already processed."},
                status=400,
            )

        payment.mark_failed()

        return Response({
            "detail": "Payment marked as FAILED.",
            "order_status": payment.order.status,
        })