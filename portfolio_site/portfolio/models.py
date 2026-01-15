from django.db import models
from wagtail.models import Page
from wagtail.fields import StreamField, RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.search import index
from wagtail import blocks
from wagtail.snippets.models import register_snippet

from .blocks import HeadingBlock, RichTextBlock, ImageBlock, CallToActionBlock, TwoColumnBlock

@register_snippet
class Technology(models.Model):
    name = models.CharField(max_length=100, verbose_name="Naam")
    icon = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Icoon"
    )

    panels = [
        FieldPanel('name'),
        FieldPanel('icon'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Technologieën'
        ordering = ['name']


class ProjectIndexPage(Page):
    intro = RichTextField(blank=True, help_text="Korte tekst over je projecten", verbose_name="Beschrijving")

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]

    subpage_types = ['portfolio.ProjectPage']
    max_count = 1

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['projects'] = ProjectPage.objects.live().child_of(self).order_by('-first_published_at')
        return context


class HomePage(Page):
    hero_title = models.CharField(max_length=100, help_text="Hoofd titel", verbose_name="Titel", default="Welkom op mijn portfolio")
    hero_subtitle = models.CharField(max_length=200, blank=True, help_text="Ondertitel onder de hoofd titel", verbose_name="Ondertitel")
    hero_image = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+', verbose_name="Achtergrond foto")
    intro_text = RichTextField(blank=True, help_text="Korte introductie tekst", verbose_name="Introductie")
    featured_projects_title = models.CharField(max_length=100, help_text="Titel voor uitgelichte projecten", verbose_name="Projecten titel", default="Uitgelichte projecten")

    # CTA button
    cta_text = models.CharField(max_length=50, blank=True, verbose_name="CTA tekst")
    cta_page = models.ForeignKey('wagtailcore.Page', null=True, blank=True, on_delete=models.SET_NULL, related_name='+', verbose_name="CTA link naar pagina")
    cta_url = models.URLField(blank=True, verbose_name="CTA externe URL")

    # CONTACT FIELDS (added)
    phone_number = models.CharField(max_length=50, blank=True, verbose_name="Telefoonnummer", help_text="Je telefoonnummer")
    email = models.EmailField(blank=True, verbose_name="E-mail", help_text="Je e-mailadres")
    linkedin_url = models.URLField(blank=True, verbose_name="LinkedIn URL", help_text="Link naar je LinkedIn profiel")

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('hero_title'),
            FieldPanel('hero_subtitle'),
            FieldPanel('hero_image'),
        ], heading="Hero sectie"),

        FieldPanel('intro_text'),
        FieldPanel('featured_projects_title'),

        MultiFieldPanel([
            FieldPanel('cta_text'),
            FieldPanel('cta_page'),
            FieldPanel('cta_url'),
        ], heading="Call to Action"),

        MultiFieldPanel([
            FieldPanel('phone_number'),
            FieldPanel('email'),
            FieldPanel('linkedin_url'),
        ], heading="Contactgegevens"),
    ]

    parent_page_types = ['wagtailcore.Page']
    max_count = 1

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['featured_projects'] = ProjectPage.objects.live().order_by('-first_published_at')[:3]
        return context


class ProjectPage(Page):
    project_date = models.DateField("Datum", null=True, blank=True)
    intro = models.TextField(max_length=500, help_text="Korte beschrijving van het project", verbose_name="Samenvatting")
    featured_image = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+', verbose_name="Hoofd foto")
    technologies = models.ManyToManyField('portfolio.Technology', blank=True, help_text="Welke technologieën heb je gebruikt?", verbose_name="Gebruikte technologieën")

    github_url = models.URLField(blank=True, help_text="Link naar GitHub", verbose_name="GitHub link")
    linkedin_url = models.URLField(blank=True, help_text="Link naar LinkedIn projectpagina", verbose_name="LinkedIn link")

    body = StreamField([
        ('heading', HeadingBlock()),
        ('paragraph', RichTextBlock()),
        ('image', ImageBlock()),
        ('call_to_action', CallToActionBlock()),
        ('two_columns', TwoColumnBlock()),
    ], use_json_field=True, verbose_name="Inhoud")

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('project_date'),
        FieldPanel('intro'),
        FieldPanel('featured_image'),
        FieldPanel('technologies'),
        MultiFieldPanel([
            FieldPanel('github_url'),
            FieldPanel('linkedin_url'),
        ], heading="Links"),
        FieldPanel('body'),
    ]

    parent_page_types = ['portfolio.ProjectIndexPage']
