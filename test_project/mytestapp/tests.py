from django.test import TestCase
from django.urls import reverse

from .models import Item
from .forms import ItemForm


class ItemModelTest(TestCase):
    def setUp(self):
        self.item = Item.objects.create(name="Test Item", description="This is a test item.")

    def test_model_can_be_saved(self):
        item_count_before = Item.objects.count()
        new_item = Item(name="New Item", description="This is a new item.")
        new_item.save()
        item_count_after = Item.objects.count()
        self.assertEqual(item_count_after, item_count_before + 1)

    def test_model_can_be_retrieved(self):
        retrieved_item = Item.objects.get(name="Test Item")
        self.assertEqual(retrieved_item.description, "This is a test item.")

    def test_model_can_be_updated(self):
        self.item.name = "Updated Item"
        self.item.description = "This item has been updated."
        self.item.save()
        updated_item = Item.objects.get(pk=self.item.pk)
        self.assertEqual(updated_item.name, "Updated Item")
        self.assertEqual(updated_item.description, "This item has been updated.")

    def test_model_can_be_deleted(self):
        item_count_before = Item.objects.count()
        self.item.delete()
        item_count_after = Item.objects.count()
        self.assertEqual(item_count_after, item_count_before - 1)


class ItemViewTest(TestCase):
    def setUp(self):
        self.item = Item.objects.create(name="Test Item", description="This is a test item.")

    def test_view_returns_status_code_200(self):
        url = reverse('item_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_view_returns_queryset_of_all_objects(self):
        url = reverse('item_list')
        response = self.client.get(url)
        items = response.context['items']
        self.assertIn(self.item, items)

    def test_view_returns_correct_template(self):
        url = reverse('item_list')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'myapp/item_list.html')


class ItemFormTest(TestCase):
    def test_valid_form_with_correct_data(self):
        form_data = {'name': 'New Item', 'description': 'This is a new item.'}
        form = ItemForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_with_incorrect_data(self):
        form_data = {'name': '', 'description': 'This is a new item.'}
        form = ItemForm(data=form_data)
        self.assertFalse(form.is_valid())


# myapp/tests.py


class ItemUpdateViewTest(TestCase):
    def setUp(self):
        self.item = Item.objects.create(name="Test Item", description="This is a test item.")

    def test_view_returns_status_code_200(self):
        url = reverse('item_update', args=[self.item.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_view_updates_object_correctly(self):
        url = reverse('item_update', args=[self.item.pk])
        updated_data = {'name': 'Updated Item', 'description': 'This item has been updated.'}
        response = self.client.post(url, data=updated_data)
        self.item.refresh_from_db()
        self.assertEqual(self.item.name, 'Updated Item')
        self.assertEqual(self.item.description, 'This item has been updated.')

    def test_view_returns_correct_template(self):
        url = reverse('item_update', args=[self.item.pk])
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'myapp/item_form.html')


class ItemDeleteViewTest(TestCase):
    def setUp(self):
        self.item = Item.objects.create(name="Test Item", description="This is a test item.")

    def test_view_returns_status_code_302(self):
        url = reverse('item_delete', args=[self.item.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_view_deletes_object_correctly(self):
        item_count_before = Item.objects.count()
        url = reverse('item_delete', args=[self.item.pk])
        response = self.client.post(url)
        item_count_after = Item.objects.count()
        self.assertEqual(item_count_after, item_count_before - 1)
