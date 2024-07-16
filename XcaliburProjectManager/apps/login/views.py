from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.views import View
from django.http import HttpRequest, HttpResponse
from django.contrib.auth import logout


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login/login.html')


# Create your views here.
class LoginView(View):
    """
    Handles user authentication and login.

    Attributes:
    - template_name (str): The name of the template for rendering the login page.
    - success_message (str): The success message displayed after a successful login.

    Methods:
    - get(request: HttpRequest) -> HttpResponse: Handles GET requests, renders the login page.
    - post(request: HttpRequest) -> HttpResponse: Handles POST requests, authenticates and logs in the user.

    """

    template_name: str = 'login/login.html'
    success_message: str = 'Welcome back '

    def get(self, request: HttpRequest) -> HttpResponse:
        """
        Handles GET requests.

        Renders the login page with an empty authentication form.

        Args:
        - request: The HTTP request object.

        Returns:
        - Rendered HTML page with the login form.

        """
        form: AuthenticationForm = AuthenticationForm()
        return render(request, self.template_name, context={"login": form})

    def post(self, request: HttpRequest) -> HttpResponse:
        """
        Handles POST requests.

        Authenticates the user and logs them in if the form is valid.

        Args:
        - request: The HTTP request object.

        Returns:
        - Redirects to the homepage after a successful login.
        - Renders the login page with error messages if authentication fails.

        """
        form: AuthenticationForm = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            username: str = form.cleaned_data.get('username')
            password: str = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, self.success_message + username)
                return redirect('projects')  # Redirect to the homepage or any other desired page after successful login
            else:
                messages.error(request, 'Invalid username or password')
                return render(request, self.template_name, context={"login": form})

        messages.error(request, 'Invalid username or password')
        return render(request, self.template_name, context={"login": form})


def login_request(request: HttpRequest) -> HttpResponse:
    """
    Handles login requests.

    Authenticates and logs in the user for POST requests.

    Args:
    - request: The HTTP request object.

    Returns:
    - Redirects to the homepage after a successful login.
    - Renders the login page with error messages if authentication fails.

    """

    if request.method == "POST":
        form: AuthenticationForm = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            username: str = form.cleaned_data.get('username')
            password: str = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("main:homepage")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")

    form: AuthenticationForm = AuthenticationForm()
    return render(request=request, template_name="login/login.html", context={"login_form": form})