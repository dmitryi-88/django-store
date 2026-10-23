from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied

from .models import Listing
from .forms import ListingForm


def listing_list(request):
    listings = Listing.objects.select_related("owner").all()
    templ = "listings/listing_list.html"
    data = {"listings": listings}

    return render(request, templ, data)


@login_required
@permission_required("listings.add_listing", raise_exception=True)
def create_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST)

        if form.is_valid():
            listing = form.save(commit=False)
            listing.owner = request.user
            listing.save()

            return redirect("listing_list")

    else:
        form = ListingForm()

    templ = "listings/listing_form.html"
    data = {"form": form}

    return render(request, templ, data)


@login_required
def edit_listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)

    if not request.user.has_perm("listings.change_listing"):
        raise PermissionDenied

    if listing.owner_id == request.user.pk:
        allowed = request.user.has_perm("listings.can_moderate_self_listing")
    else:
        allowed = request.user.has_perm("listings.can_moderate_listing")

    if not allowed:
        raise PermissionDenied

    if request.method == "POST":
        form = ListingForm(request.POST, instance=listing)

        if form.is_valid():
            form.save()
            return redirect("listing_list")
    else:
        form = ListingForm(instance=listing)

    return render(
        request,
        "listings/listing_form.html",
        {"form": form, "listing": listing},
    )


@login_required
def delete_listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)

    if not request.user.has_perm("listings.delete_listing"):
        raise PermissionDenied

    if listing.owner_id != request.user.pk and not request.user.has_perm(
        "listings.can_moderate_listing"
    ):
        raise PermissionDenied

    if request.method == "POST":
        listing.delete()
        return redirect("listing_list")

    return render(
        request,
        "listings/listing_confirm_delete.html",
        {"listing": listing},
    )
