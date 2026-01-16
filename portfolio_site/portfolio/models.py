# Nodig om data in de database op te slaan
from django.db import models

# Basis voor alle pagina’s in Wagtail
from wagtail.models import Page

# Velden voor tekst en flexibele inhoud
from wagtail.fields import StreamField, RichTextField

# Zorgt voor de layout in het admin scherm
from wagtail.admin.panels import FieldPanel, MultiFieldPanel

# Voor zoeken in de website
from wagtail.search import index

# Voor het maken van content blokken
from wagtail import blocks

# Voor herbruikbare data (snippets)
from wagtail.snippets.models import register_snippet

# Zelf gemaakte blokken voor StreamField
from .blocks import (
    HeadingBlock,
    RichTextBlock,
    ImageBlock,
    CallToActionBlock,
    TwoColumnBlock
)

# =========================
# TECHNOLOGIE (SNIPPET)
# =========================

@register_snippet
class Technology(models.Model):
    # Naam van de technologie
    name = models.CharField(max_length=100)

    # Optioneel icoon bij de technologie
    icon = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    # Wat je ziet in het admin scherm
    panels = [
        FieldPanel('name'),
        FieldPanel('icon'),
    ]

    # Hoe de naam wordt getoond in lijsten
    def __str__(self):
        return self.name

    class Meta:
        # Meervoudige naam in admin
        verbose_name_plural = 'Technologieën'
        # Sorteren op naam
        ordering = ['name']


# =========================
# PROJECT OVERZICHT PAGINA
# =========================

class ProjectIndexPage(Page):
    # Korte tekst boven de projecten
    intro = RichTextField(blank=True)

    # Velden in het admin scherm
    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]

    # Alleen project pagina’s mogen hieronder staan
    subpage_types = ['portfolio.ProjectPage']

    # Er mag maar één overzicht pagina zijn
    max_count = 1

    # Extra data voor de template
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        # Haalt alle gepubliceerde projecten op
        context['projects'] = (
            ProjectPage.objects
            .live()
            .child_of(self)
            .order_by('-first_published_at')
        )
        return context


# =========================
# HOMEPAGE
# =========================

class HomePage(Page):
    # Titel bovenaan de homepage
    hero_title = models.CharField(
        max_length=100,
        default="Welkom op mijn portfolio"
    )

    # Kleine tekst onder de titel
    hero_subtitle = models.CharField(
        max_length=200,
        blank=True
    )

    # Achtergrond afbeelding
    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    # Introductie tekst
    intro_text = RichTextField(blank=True)

    # Titel boven uitgelichte projecten
    featured_projects_title = models.CharField(
        max_length=100,
        default="Uitgelichte projecten"
    )

    # Call To Action knop
    cta_text = models.CharField(max_length=50, blank=True)
    cta_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    cta_url = models.URLField(blank=True)

    # Contact gegevens
    phone_number = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    linkedin_url = models.URLField(blank=True)

    # Indeling van het admin scherm
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('hero_title'),
            FieldPanel('hero_subtitle'),
            FieldPanel('hero_image'),
        ], heading="Hero"),

        FieldPanel('intro_text'),
        FieldPanel('featured_projects_title'),

        MultiFieldPanel([
            FieldPanel('cta_text'),
            FieldPanel('cta_page'),
            FieldPanel('cta_url'),
        ], heading="Knop"),

        MultiFieldPanel([
            FieldPanel('phone_number'),
            FieldPanel('email'),
            FieldPanel('linkedin_url'),
        ], heading="Contact"),
    ]

    # Homepage staat bovenaan de site
    parent_page_types = ['wagtailcore.Page']

    # Er mag maar één homepage zijn
    max_count = 1

    # Projecten tonen op de homepage
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        # De 3 nieuwste projecten
        context['featured_projects'] = (
            ProjectPage.objects
            .live()
            .order_by('-first_published_at')[:3]
        )
        return context


# =========================
# PROJECT PAGINA
# =========================

class ProjectPage(Page):
    # Datum van het project
    project_date = models.DateField(null=True, blank=True)

    # Korte uitleg over het project
    intro = models.TextField(max_length=500)

    # Hoofd afbeelding
    featured_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    # Gebruikte technologieën
    technologies = models.ManyToManyField(
        'portfolio.Technology',
        blank=True
    )

    # Links naar andere websites
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)

    # Inhoud die je zelf kunt opbouwen
    body = StreamField([
        ('heading', HeadingBlock()),
        ('paragraph', RichTextBlock()),
        ('image', ImageBlock()),
        ('call_to_action', CallToActionBlock()),
        ('two_columns', TwoColumnBlock()),
    ], use_json_field=True)

    # Velden die gebruikt worden bij zoeken
    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    # Velden in het admin scherm
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

    # Project pagina’s moeten onder het overzicht staan
    parent_page_types = ['portfolio.ProjectIndexPage']
