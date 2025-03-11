#
# Conditional build:
%bcond_without	tests	# unit tests

%define		module		responses
Summary:	A utility for mocking out the Python Requests library
Summary(pl.UTF-8):	Narzędzie do podstawiania atrap biblioteki Python Requests
Name:		python3-%{module}
Version:	0.22.0
Release:	3
License:	Apache v2.0
Group:		Libraries/Python
#Source0Download: https://github.com/getsentry/responses/releases
Source0:	https://github.com/getsentry/responses/archive/%{version}/%{module}-%{version}.tar.gz
# Source0-md5:	87376da806d05a4de46e9b6a868d7ece
URL:		https://github.com/getsentry/responses
BuildRequires:	python3-modules >= 1:3.7
BuildRequires:	python3-setuptools
%if %{with tests}
#BuildRequires:	python3-coverage >= 6.0.0
BuildRequires:	python3-flake8
BuildRequires:	python3-pytest >= 7.0.0
BuildRequires:	python3-pytest-asyncio
#BuildRequires:	python3-pytest-cov
BuildRequires:	python3-pytest-httpserver
BuildRequires:	python3-requests >= 2.22.0
BuildRequires:	python3-requests < 3
BuildRequires:	python3-toml
BuildRequires:	python3-types-toml
%if "%{py3_ver}" == "3.7"
BuildRequires:	python3-typing-extensions
%endif
BuildRequires:	python3-urllib3 >= 1.25.10
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A utility library for mocking out the requests Python library.

%description -l pl.UTF-8
Biblioteka narzędziowa do podstawiania atrap biblioteki Pythona
requests.

%prep
%setup -q -n %{module}-%{version}

%build
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS="pytest_asyncio.plugin,pytest_httpserver.pytest_plugin" \
%{__python3} -m pytest responses
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/responses/tests

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES README.rst
%{py3_sitescriptdir}/responses
%{py3_sitescriptdir}/responses-%{version}-py*.egg-info
