%define		php_name	php%{?php_suffix}
%define		modname	spidermonkey
%define		status		stable
Summary:	%{modname} - Spidermonkey JavaScript engine for PHP
Summary(pl.UTF-8):	%{modname} - silnik JavaScript Spidermonkey dla PHP
Name:		%{php_name}-pecl-%{modname}
Version:	1.0.0
Release:	3
License:	PHP 3.01
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
# Source0-md5:	1a7a4043fa6c86bb7e3cb24e794c284b
Patch0:		lib64.patch
URL:		http://pecl.php.net/package/spidermonkey
BuildRequires:	%{php_name}-devel >= 4:5.3.0
BuildRequires:	js185-devel
BuildRequires:	rpmbuild(macros) >= 1.650
%{?requires_php_extension}
Requires:	php(core) >= 5.3.0
Provides:	php(%{modname}) = %{version}
Obsoletes:	php-pear-%{modname}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This extension allow you to embed Mozilla's Javascript engine
Spidermonkey in PHP.

In PECL status of this package is: %{status}.

%description -l pl.UTF-8
To rozszerzenie pozwala na osadzanie w PHP silnika Javascript Mozilli
- Spidermonkey.

To rozszerzenie ma w PECL status: %{status}.

%prep
%setup -q -c
%ifarch %{x8664}
%patch0 -p1
%endif
mv %{modname}-%{version}/* .

%build
# libtool 2.2 build fix
if [ -f '%{_aclocaldir}/ltsugar.m4' ]; then
	cat "%{_aclocaldir}/ltsugar.m4" >> "config.m4"
	cat "%{_aclocaldir}/ltversion.m4" >> "config.m4"
	cat "%{_aclocaldir}/lt~obsolete.m4" >> "config.m4"
	cat "%{_aclocaldir}/ltoptions.m4" >> "config.m4"
fi

phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{php_sysconfdir}/conf.d,%{php_extensiondir}}

install modules/%{modname}.so $RPM_BUILD_ROOT%{php_extensiondir}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini
; Enable %{modname} extension module
extension=%{modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
