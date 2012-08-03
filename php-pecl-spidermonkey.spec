%define		_modname	spidermonkey
%define		_status		beta
Summary:	%{_modname} - Spidermonkey JavaScript engine for PHP
Summary(pl.UTF-8):	%{_modname} - silnik JavaScript Spidermonkey dla PHP
Name:		php-pecl-%{_modname}
Version:	0.1.4
Release:	2
License:	PHP 3.01
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{_modname}-%{version}.tgz
# Source0-md5:	4f4a9d3558d1354e728ab168e11c35c5
URL:		http://pecl.php.net/package/%{_modname}/
BuildRequires:	js-devel >= 1.7
BuildRequires:	php-devel >= 4:5.3.0
BuildRequires:	rpmbuild(macros) >= 1.344
%{?requires_php_extension}
Requires:	php-common >= 4:5.3.0
Obsoletes:	php-pear-%{_modname}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This extension allow you to embed Mozilla's Javascript engine
Spidermonkey in PHP.

In PECL status of this package is: %{_status}.

%description -l pl.UTF-8
To rozszerzenie pozwala na osadzanie w PHP silnika Javascript Mozilli
- Spidermonkey.

To rozszerzenie ma w PECL status: %{_status}.

%prep
%setup -q -c
mv %{_modname}-%{version}/* .

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

install modules/%{_modname}.so $RPM_BUILD_ROOT%{php_extensiondir}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{_modname}.ini
; Enable %{_modname} extension module
extension=%{_modname}.so
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
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{_modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{_modname}.so
