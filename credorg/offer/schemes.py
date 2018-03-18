import coreapi
from rest_framework.compat import coreschema
from rest_framework.schemas import AutoSchema


class AuthViewSchema(AutoSchema):
    def get_link(self, path, method, base_url):
        links = super(AuthViewSchema, self).get_link(path, method, base_url)

        if method == 'POST':
            return coreapi.Link(
                action='post',
                url=path,
                fields=[
                    coreapi.Field(
                        "username",
                        description="Username",
                        example="asdasd",
                        required=True,
                        location="form",
                        schema=coreschema.String()
                    ),
                    coreapi.Field(
                        "password",
                        description="Password",
                        required=True,
                        location="form",
                        schema=coreschema.String()
                    ),
                ]
            )

        return links


class PartnerViewSchema(AutoSchema):
    def get_link(self, path, method, base_url):
        links = super(PartnerViewSchema, self).get_link(path, method, base_url)

        if method == 'POST':
            if path.strip('/').endswith('Worksheets'):
                return coreapi.Link(
                    action='post',
                    url=path,
                    fields=[
                        coreapi.Field(
                            "rotation_from",
                            description="Rotation from",
                            required=True,
                            location="form",
                            schema=coreschema.String()
                        ),
                        coreapi.Field(
                            "rotation_to",
                            description="Rotation to",
                            required=True,
                            location="form",
                            schema=coreschema.String()
                        ),
                        coreapi.Field(
                            "name",
                            description="Name",
                            required=True,
                            location="form",
                            schema=coreschema.String()
                        ),
                        coreapi.Field(
                            "offer_type",
                            description="Offer type",
                            required=True,
                            location="form",
                            schema=coreschema.Integer()
                        ),
                        coreapi.Field(
                            "score_min",
                            description="Score Min",
                            required=True,
                            location="form",
                            schema=coreschema.Integer()
                        ),
                        coreapi.Field(
                            "score_max",
                            description="Score Max",
                            required=True,
                            location="form",
                            schema=coreschema.Integer()
                        ),
                        coreapi.Field(
                            "credit_organization",
                            description="Credit organization Id",
                            required=True,
                            location="form",
                            schema=coreschema.Integer()
                        ),
                    ]
                )

            elif path.strip('/').endswith('Orders'):
                return coreapi.Link(
                    action='post',
                    url=path,
                    fields=[
                        coreapi.Field(
                            "worksheet",
                            description="Worksheet Id",
                            required=True,
                            location="form",
                            schema=coreschema.Integer()
                        ),
                        coreapi.Field(
                            "offer",
                            description="Offer Id",
                            required=True,
                            location="form",
                            schema=coreschema.Integer()
                        ),
                    ]
                )

            elif path.strip('/').endswith('SendOrder'):
                return coreapi.Link(
                    action='post',
                    url=path,
                    fields=[
                        coreapi.Field(
                            "order",
                            description="Order Id",
                            required=True,
                            location="form",
                            schema=coreschema.Integer()
                        ),
                    ]
                )

        return links


class CreditOrganizationViewSchema(AutoSchema):
    def get_link(self, path, method, base_url):
        links = super(CreditOrganizationViewSchema, self).get_link(
            path, method, base_url)

        if method == 'PUT':
            if path.strip('/').endswith('Status'):
                return coreapi.Link(
                    action='put',
                    url=path,
                    fields=[
                        coreapi.Field(
                            "order",
                            required=True,
                            location="form",
                            schema=coreschema.Integer()
                        ),
                        coreapi.Field(
                            "status",
                            required=True,
                            location="form",
                            schema=coreschema.Integer()
                        ),
                    ]
                )

        return links


