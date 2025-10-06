from django.shortcuts import render, redirect

from .models import Product, ProductImage
from .forms import EditProductForm, ProductImagesFormSet

def product(request):
    pass

def edit_product(request, id):

    product = Product.objects.get(id = id)
    product_images = ProductImage.objects.filter(product = product)

    if request.method == "POST":
        form = EditProductForm(request.POST, instance=product)
        formset = ProductImagesFormSet(request.POST, request.FILES, queryset=product_images)

        if formset.is_valid():
            for form in formset.deleted_forms:
                if form.instance.pk:
                    form.instance.delete()

            new_instances = formset.save(commit=False)  # Save new instances manually
            for instance in new_instances:
                if not instance.product_id:  # Only apply to new images
                    instance.product = product  # Assign the product
                    instance.save()  # Save the new image

            return redirect("edit_product", id=id)  # Redirect to avoid resubmission issues
        else:
            print(form.errors)
            print("Formset Errors:", formset.errors)  # Debugging
    else:
        form = EditProductForm(instance=product)
        formset = ProductImagesFormSet(queryset=product_images)

    return render(request, "products.edit.html", { 
        "form": form,
        "images": formset
    })
