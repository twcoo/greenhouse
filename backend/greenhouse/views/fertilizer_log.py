from typing import Any, Optional, cast

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request

from ..models import Fertilizer, FertilizerLog
from ..openapi.fertilizer_log.examples import (
    CREATE_FERTILIZER_LOG_REQUEST_EXAMPLE,
    PARTIAL_UPDATE_FERTILIZER_LOG_REQUEST_EXAMPLE,
    UPDATE_FERTILIZER_LOG_REQUEST_EXAMPLE)
from ..openapi.fertilizer_log.parameters import (FERTILIZER_LOG_ID_PARAM,
                                                 FERTILIZER_PK_PARAM)
from ..openapi.fertilizer_log.responses import (
    FERTILIZER_LOG_CREATE_VALIDATION_RESPONSE, FERTILIZER_LOG_CREATED_RESPONSE,
    FERTILIZER_LOG_DELETE_RESPONSE, FERTILIZER_LOG_LIST_RESPONSE,
    FERTILIZER_LOG_NOT_FOUND_RESPONSE, FERTILIZER_LOG_PARTIAL_UPDATE_RESPONSE,
    FERTILIZER_LOG_PARTIAL_UPDATE_VALIDATION_RESPONSE,
    FERTILIZER_LOG_UPDATE_RESPONSE, FERTILIZER_LOG_UPDATE_VALIDATION_RESPONSE)
from ..serializers import FertilizerLogSerializer
from ..utils.api import CustomAuthentication


def _normalize_ingredient(value: Optional[str]) -> str:
    return (value or "").strip()


def _add_ingredient(fertilizer: Fertilizer, item_added: Optional[str]) -> None:
    item_added = _normalize_ingredient(item_added)
    if not item_added:
        return

    ingredients = list(fertilizer.ingredients or [])
    if any(item.casefold() == item_added.casefold() for item in ingredients):
        return

    log_added = list(fertilizer.log_added_ingredients or [])
    log_added.append(item_added)

    ingredients.append(item_added)
    fertilizer.ingredients = ingredients
    fertilizer.log_added_ingredients = log_added
    fertilizer.save(
        update_fields=["ingredients", "log_added_ingredients", "updated_at"]
    )


def _remove_ingredient_if_unreferenced(
    fertilizer: Fertilizer,
    item_added: Optional[str],
    exclude_pk: Optional[int] = None,
) -> None:
    item_added = _normalize_ingredient(item_added)
    if not item_added:
        return

    log_added = list(fertilizer.log_added_ingredients or [])
    if not any(item.casefold() == item_added.casefold() for item in log_added):
        return

    referenced = FertilizerLog.objects.filter(
        fertilizer=fertilizer,
        event_type="ADDED_INGREDIENT",
        item_added__iexact=item_added,
    )
    if exclude_pk is not None:
        referenced = referenced.exclude(pk=exclude_pk)

    if referenced.exists():
        return

    fertilizer.ingredients = [
        item
        for item in (fertilizer.ingredients or [])
        if item.casefold() != item_added.casefold()
    ]
    fertilizer.log_added_ingredients = [
        item for item in log_added if item.casefold() != item_added.casefold()
    ]
    fertilizer.save(
        update_fields=["ingredients", "log_added_ingredients", "updated_at"]
    )


@extend_schema_view(
    get=extend_schema(
        tags=["Fertilizer Log"],
        summary="List fertilizer logs",
        description=(
            "Returns a paginated list of log entries for the "
            "specified fertilizer, ordered most recent first. Results are "
            "scoped to the authenticated user."
        ),
        parameters=FERTILIZER_PK_PARAM,
        responses={
            200: FERTILIZER_LOG_LIST_RESPONSE,
            404: FERTILIZER_LOG_NOT_FOUND_RESPONSE,
        },
    ),
    post=extend_schema(
        tags=["Fertilizer Log"],
        summary="Log a fertilizer entry",
        description=("Log a new entry for the specified fertilizer."),
        parameters=FERTILIZER_PK_PARAM,
        examples=[CREATE_FERTILIZER_LOG_REQUEST_EXAMPLE],
        responses={
            201: FERTILIZER_LOG_CREATED_RESPONSE,
            400: FERTILIZER_LOG_CREATE_VALIDATION_RESPONSE,
            404: FERTILIZER_LOG_NOT_FOUND_RESPONSE,
        },
    ),
)
class FertilizerLogListApiView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericAPIView,
):
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = FertilizerLogSerializer

    def _get_fertilizer(self) -> Fertilizer:
        return cast(
            Fertilizer,
            get_object_or_404(
                Fertilizer,
                pk=self.kwargs["fertilizer_pk"],
                user=self.request.user,
            ),
        )

    def get_queryset(self):
        return FertilizerLog.objects.filter(
            fertilizer=self._get_fertilizer()
        ).order_by("-log_date", "-pk")

    def perform_create(self, serializer):
        fertilizer = self._get_fertilizer()
        serializer.save(fertilizer=fertilizer)

        validated_data = serializer.validated_data
        if validated_data.get("event_type") == "ADDED_INGREDIENT":
            _add_ingredient(fertilizer, validated_data.get("item_added"))

    def get(self, request: Request, *args: Any, **kwargs: Any):
        return self.list(request, *args, **kwargs)

    def post(self, request: Request, *args: Any, **kwargs: Any):
        return self.create(request, *args, **kwargs)


@extend_schema_view(
    put=extend_schema(
        tags=["Fertilizer Log"],
        summary="Update a fertilizer log",
        description="Updates an existing fertilizer log entry by ID.",
        parameters=FERTILIZER_LOG_ID_PARAM,
        examples=[UPDATE_FERTILIZER_LOG_REQUEST_EXAMPLE],
        responses={
            200: FERTILIZER_LOG_UPDATE_RESPONSE,
            400: FERTILIZER_LOG_UPDATE_VALIDATION_RESPONSE,
            404: FERTILIZER_LOG_NOT_FOUND_RESPONSE,
        },
    ),
    patch=extend_schema(
        tags=["Fertilizer Log"],
        summary="Partially update a fertilizer log",
        description=(
            "Partially updates an existing fertilizer log entry by ID. "
            "Only the fields provided will be updated."
        ),
        parameters=FERTILIZER_LOG_ID_PARAM,
        examples=[PARTIAL_UPDATE_FERTILIZER_LOG_REQUEST_EXAMPLE],
        responses={
            200: FERTILIZER_LOG_PARTIAL_UPDATE_RESPONSE,
            400: FERTILIZER_LOG_PARTIAL_UPDATE_VALIDATION_RESPONSE,
            404: FERTILIZER_LOG_NOT_FOUND_RESPONSE,
        },
    ),
    delete=extend_schema(
        tags=["Fertilizer Log"],
        summary="Delete a fertilizer log",
        description="Deletes an existing fertilizer log entry by ID.",
        parameters=FERTILIZER_LOG_ID_PARAM,
        responses={
            204: FERTILIZER_LOG_DELETE_RESPONSE,
            404: FERTILIZER_LOG_NOT_FOUND_RESPONSE,
        },
    ),
)
class FertilizerLogDetailApiView(
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericAPIView,
):
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = FertilizerLogSerializer

    def _get_fertilizer(self) -> Fertilizer:
        return cast(
            Fertilizer,
            get_object_or_404(
                Fertilizer,
                pk=self.kwargs["fertilizer_pk"],
                user=self.request.user,
            ),
        )

    def get_queryset(self):
        return FertilizerLog.objects.filter(fertilizer=self._get_fertilizer())

    def perform_update(self, serializer):
        instance = serializer.instance
        old_event_type = instance.event_type
        old_item_added = instance.item_added

        serializer.save()

        new_event_type = serializer.validated_data.get(
            "event_type", old_event_type
        )
        new_item_added = serializer.validated_data.get(
            "item_added", old_item_added
        )

        fertilizer = instance.fertilizer

        old_item = _normalize_ingredient(old_item_added)
        if old_event_type == "ADDED_INGREDIENT" and old_item:
            new_item = _normalize_ingredient(new_item_added)
            if (
                new_event_type != "ADDED_INGREDIENT"
                or new_item.casefold() != old_item.casefold()
            ):
                _remove_ingredient_if_unreferenced(
                    fertilizer, old_item_added, exclude_pk=instance.pk
                )

        if new_event_type == "ADDED_INGREDIENT":
            _add_ingredient(fertilizer, new_item_added)

    def perform_destroy(self, instance):
        fertilizer = instance.fertilizer
        event_type = instance.event_type
        item_added = instance.item_added

        instance.delete()

        if event_type == "ADDED_INGREDIENT":
            _remove_ingredient_if_unreferenced(fertilizer, item_added)

    def put(self, request: Request, *args: Any, **kwargs: Any):
        return self.update(request, *args, **kwargs)

    def patch(self, request: Request, *args: Any, **kwargs: Any):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request: Request, *args: Any, **kwargs: Any):
        return self.destroy(request, *args, **kwargs)
