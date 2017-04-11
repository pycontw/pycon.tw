from import_export import fields, resources

from .models import Review


class ReviewResource(resources.ModelResource):

    reviewer = fields.Field(
        attribute='reviewer__email',
        readonly=True,
    )
    proposal = fields.Field(
        attribute='proposal__title',
        readonly=True,
    )

    class Meta:
        model = Review
        fields = [
            'id', 'reviewer', 'proposal', 'stage', 'vote', 'comment',
            'discloses_comment', 'appropriateness',
        ]
        export_order = fields

    def dehydrate_discloses_comment(self, instance):
        return int(instance.discloses_comment)

    def dehydrate_appropriateness(self, instance):
        return int(instance.appropriateness)
