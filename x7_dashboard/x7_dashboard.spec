%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%endif

%define mod_name x7_dashboard

Name:             x7_dashboard
Version:          0.0.1
Release:          1
Summary:          Django based interface for vms-manage
License:          GNU GPL v3
Vendor:           Grid Dynamics International, Inc.
URL:              http://www.vonbros.com/
Group:            Development/Languages/Python

Source0:          %{name}-%{version}.tar.gz
BuildRoot:        %{_tmppath}/%{name}-%{version}-build
BuildRequires:    python-devel python-setuptools
BuildArch:        noarch
Requires:         steer

%description

This package contains the web interface for vms manage.


%prep
%setup -q -n %{name}-%{version}

%build
%{__python} setup.py build

%install
%__rm -rf %{buildroot}

%{__python} setup.py install -O1 --skip-build --prefix=%{_prefix} --root=%{buildroot}

%clean
%__rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README
%{python_sitelib}/%{mod_name}*


%changelog
