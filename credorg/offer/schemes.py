from __future__ import absolute_import, unicode_literals
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
                            "last_name",
                            required=True,
                            location="form",
                            schema=coreschema.String()
                        ),
                        coreapi.Field(
                            "first_name",
                            required=True,
                            location="form",
                            schema=coreschema.String()
                        ),
                        coreapi.Field(
                            "middle_name",
                            required=True,
                            location="form",
                            schema=coreschema.String()
                        ),
                        coreapi.Field(
                            "dob",
                            required=True,
                            location="form",
                            schema=coreschema.String()
                        ),
                        coreapi.Field(
                            "phone_number",
                            required=True,
                            location="form",
                            schema=coreschema.String()
                        ),
                        coreapi.Field(
                            "passport_number",
                            required=True,
                            location="form",
                            schema=coreschema.String()
                        ),
                        coreapi.Field(
                            "score",
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

        elif method == 'GET':
            if path.strip('/').endswith('Worksheets'):
                return coreapi.Link(
                    action='get',
                    url=path,
                    description="""
                    Use model kind filter:
                    __exact,
                    __startswith,
                    __in,
                    __gte, __gt, __lte, __lt,
                    ...
                    """,
                    fields=[
                        coreapi.Field(
                            "last_name",
                            required=False,
                            location="query",
                            schema=coreschema.String()
                        ),
                        coreapi.Field(
                            "first_name",
                            required=False,
                            location="query",
                            schema=coreschema.String()
                        ),
                        coreapi.Field(
                            "middle_name",
                            required=False,
                            location="query",
                            schema=coreschema.String()
                        ),
                        coreapi.Field(
                            "dob",
                            required=False,
                            location="query",
                            schema=coreschema.String()
                        ),
                        coreapi.Field(
                            "phone_number",
                            required=False,
                            location="query",
                            schema=coreschema.String()
                        ),
                        coreapi.Field(
                            "passport_number",
                            required=False,
                            location="query",
                            schema=coreschema.String()
                        ),
                        coreapi.Field(
                            "score",
                            required=False,
                            location="query",
                            schema=coreschema.Integer()
                        ),
                        coreapi.Field(
                            "order_by",
                            required=False,
                            location="query",
                            schema=coreschema.String()
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

        elif method == 'POST':
            if path.strip('/').endswith('Offers'):
                return coreapi.Link(
                    action='post',
                    url=path,
                    fields=[
                        coreapi.Field(
                            "rotation_from",
                            required=True,
                            location="form",
                            schema=coreschema.String()
                        ),
                        coreapi.Field(
                            "rotation_to",
                            required=True,
                            location="form",
                            schema=coreschema.String()
                        ),
                        coreapi.Field(
                            "name",
                            required=True,
                            location="form",
                            schema=coreschema.String()
                        ),
                        coreapi.Field(
                            "offer_type",
                            required=True,
                            location="form",
                            schema=coreschema.Integer()
                        ),
                        coreapi.Field(
                            "score_min",
                            required=True,
                            location="form",
                            schema=coreschema.Integer()
                        ),
                        coreapi.Field(
                            "score_max",
                            required=True,
                            location="form",
                            schema=coreschema.Integer()
                        ),
                    ]
                )

        return links


