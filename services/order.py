from __future__ import annotations

from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket

User = get_user_model()


@transaction.atomic
def create_order(
    tickets: list[dict],
    username: str,
    date: str | None = None,
) -> None:
    user = User.objects.get(username=username)

    order = Order(user=user)
    order.save()

    if date:
        parsed = datetime.strptime(date, "%Y-%m-%d %H:%M")
        Order.objects.filter(pk=order.pk).update(created_at=parsed)

    for t in tickets:
        Ticket.objects.create(
            movie_session_id=t["movie_session"],
            order=order,
            row=t["row"],
            seat=t["seat"],
        )


def get_orders(username: str | None = None) -> QuerySet[Order]:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(user__username=username)
    return queryset
