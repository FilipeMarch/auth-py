import pytest
from faker import Faker

from gotrue import AsyncGoTrueApi
from gotrue.constants import COOKIE_OPTIONS, GOTRUE_URL
from gotrue.types import CookieOptions, LinkType, User

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwicm9sZSI6InN1cGFiYXNlX2FkbWluIiwiaWF0IjoxNTE2MjM5MDIyfQ.0sOtTSTfPv5oPZxsjvBO249FI4S4p0ymHoIZ6H6z9Y8"  # noqa: E501


def create_api() -> AsyncGoTrueApi:
    return AsyncGoTrueApi(
        url=GOTRUE_URL,
        headers={"Authorization": f"Bearer {token}"},
        cookie_options=CookieOptions.from_dict(COOKIE_OPTIONS),
    )


fake = Faker()

email = f"api_ac_disabled_{fake.email().lower()}"
password = fake.password()


@pytest.mark.asyncio
async def test_sign_up_with_email_and_password():
    try:
        api = create_api()
        response = await api.sign_up_with_email(
            email,
            password,
            redirect_to="https://localhost:9999/welcome",
            data={"status": "alpha"},
        )
        assert isinstance(response, User)
    except Exception:
        assert False


email2 = f"api_generate_link_signup_{fake.email().lower()}"
password2 = fake.password()


@pytest.mark.asyncio
async def test_generate_sign_up_link():
    try:
        api = create_api()
        response = await api.generate_link(
            type=LinkType.signup,
            email=email2,
            password=password2,
            redirect_to="https://localhost:9999/welcome",
            data={"status": "alpha"},
        )
        assert isinstance(response, User)
    except Exception:
        assert False


email3 = f"api_generate_link_signup_{fake.email().lower()}"


@pytest.mark.asyncio
async def test_generate_magic_link():
    try:
        api = create_api()
        response = await api.generate_link(
            type=LinkType.magiclink,
            email=email3,
            redirect_to="https://localhost:9999/welcome",
        )
        assert isinstance(response, User)
    except Exception:
        assert False


@pytest.mark.asyncio
async def test_generate_invite_link():
    try:
        api = create_api()
        response = await api.generate_link(
            type=LinkType.invite,
            email=email3,
            redirect_to="https://localhost:9999/welcome",
        )
        assert isinstance(response, User)
    except Exception:
        assert False


@pytest.mark.asyncio
@pytest.mark.depends(on=[test_sign_up_with_email_and_password.__name__])
async def test_generate_recovery_link():
    try:
        api = create_api()
        response = await api.generate_link(
            type=LinkType.recovery,
            email=email,
            redirect_to="https://localhost:9999/welcome",
        )
        assert isinstance(response, User)
    except Exception:
        assert False
