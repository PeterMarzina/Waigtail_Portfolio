from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from django.utils.translation import gettext_lazy as _


class HeadingBlock(blocks.StructBlock):
    heading_text = blocks.CharBlock(required=True, help_text=_("Schrijf je titel hier"), label=_("Titel"))
    size = blocks.ChoiceBlock(
        choices=[
            ('h2', 'Groot'),
            ('h3', 'Medium'),
            ('h4', 'Klein'),
        ],
        default='h2',
        help_text=_("Hoe groot moet de titel zijn?"),
        label=_("Grootte")
    )

    class Meta:
        template = 'portfolio/blocks/heading_block.html'
        icon = 'title'
        label = _('Titel')


class RichTextBlock(blocks.RichTextBlock):
    class Meta:
        template = 'portfolio/blocks/richtext_block.html'
        icon = 'doc-full'
        label = _('Tekst')


class ImageBlock(blocks.StructBlock):
    image = ImageChooserBlock(required=True, label=_("Foto"))
    caption = blocks.CharBlock(required=False, label=_("Onderschrift"))
    attribution = blocks.CharBlock(required=False, label=_("Bron"))

    class Meta:
        template = 'portfolio/blocks/image_block.html'
        icon = 'image'
        label = _('Foto')


from wagtail import blocks

class CallToActionBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True, help_text="Titel van de CTA")
    page = blocks.PageChooserBlock(required=False, help_text="Kies een interne pagina")
    url = blocks.URLBlock(required=False, help_text="Of externe URL")
    button_text = blocks.CharBlock(default="Lees meer", help_text="Tekst op de knop")

    class Meta:
        icon = "link"
        label = "Call to Action"
        template = "blocks/call_to_action_block.html"


class TwoColumnBlock(blocks.StructBlock):
    left_column = blocks.StreamBlock([
        ('heading', HeadingBlock()),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageBlock()),
    ], icon='arrow-left', label=_('Linker kant'))

    right_column = blocks.StreamBlock([
        ('heading', HeadingBlock()),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageBlock()),
    ], icon='arrow-right', label=_('Rechter kant'))

    class Meta:
        template = 'portfolio/blocks/two_column_block.html'
        icon = 'horizontalrule'
        label = _('Twee kolommen')