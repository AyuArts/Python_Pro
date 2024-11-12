from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Ad

class AdListView(ListView):
    """
    Представление для отображения списка активных объявлений.

    Атрибуты:
    ----------
    model : Model
        Модель, с которой работает представление.
    template_name : str
        Путь к HTML-шаблону для отображения списка объявлений.
    context_object_name : str
        Имя переменной контекста, в которой будут доступны объявления в шаблоне.
    queryset : QuerySet
        Запрос, который возвращает только активные объявления.
    """

    model = Ad
    template_name = 'board/ad_list.html'
    context_object_name = 'ads'
    queryset = Ad.objects.filter(is_active=True)


class AdDetailView(DetailView):
    """
    Представление для отображения детальной информации о конкретном объявлении.

    Атрибуты:
    ----------
    model : Model
        Модель, с которой работает представление.
    template_name : str
        Путь к HTML-шаблону для отображения деталей объявления.
    context_object_name : str
        Имя переменной контекста, в которой будет доступно объявление в шаблоне.
    """

    model = Ad
    template_name = 'board/ad_detail.html'
    context_object_name = 'ad'


class AdCreateView(CreateView):
    """
    Представление для создания нового объявления.

    Атрибуты:
    ----------
    model : Model
        Модель, с которой работает представление.
    template_name : str
        Путь к HTML-шаблону для формы создания объявления.
    fields : list
        Список полей модели, которые будут отображаться в форме.
    success_url : str
        URL для перенаправления после успешного создания объявления.
    """

    model = Ad
    template_name = 'board/ad_form.html'
    fields = ['title', 'description', 'price', 'category']
    success_url = reverse_lazy('board:ad_list')

    def form_valid(self, form):
        """
        Переопределение метода form_valid для добавления пользователя,
        создавшего объявление.

        :param form: Форма с данными объявления.
        :return: Результат выполнения родительского метода form_valid.
        """
        form.instance.user = self.request.user
        return super().form_valid(form)


class AdUpdateView(UpdateView):
    """
    Представление для редактирования существующего объявления.

    Атрибуты:
    ----------
    model : Model
        Модель, с которой работает представление.
    template_name : str
        Путь к HTML-шаблону для формы редактирования объявления.
    fields : list
        Список полей модели, которые будут отображаться в форме.
    success_url : str
        URL для перенаправления после успешного обновления объявления.
    """

    model = Ad
    template_name = 'board/ad_form.html'
    fields = ['title', 'description', 'price', 'category']
    success_url = reverse_lazy('board:ad_list')


class AdDeleteView(DeleteView):
    """
    Представление для удаления объявления.

    Атрибуты:
    ----------
    model : Model
        Модель, с которой работает представление.
    template_name : str
        Путь к HTML-шаблону для подтверждения удаления объявления.
    success_url : str
        URL для перенаправления после успешного удаления объявления.
    """

    model = Ad
    template_name = 'board/ad_confirm_delete.html'
    success_url = reverse_lazy('board:ad_list')
