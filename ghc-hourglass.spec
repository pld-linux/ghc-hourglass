#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	hourglass
Summary:	Simple performant time related library
Name:		ghc-%{pkgname}
Version:	0.2.12
Release:	2
License:	BSD
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/hourglass
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	73b123130a9d1c3c096c6895e3a4915f
URL:		http://hackage.haskell.org/package/hourglass
BuildRequires:	ghc >= 6.12.3
%if %{with prof}
BuildRequires:	ghc-prof
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
%requires_eq	ghc
Requires(post,postun):	/usr/bin/ghc-pkg
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
Simple time library focusing on simple but powerful and performant
API.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description prof
Profiling %{pkgname} library for GHC.  Should be installed when
GHC's profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.hs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build
runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc CHANGELOG.md README.md %{name}-%{version}-doc/*
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.so
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.a
%exclude %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a

%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Hourglass
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Hourglass/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Hourglass/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Hourglass/Internal
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Hourglass/Internal/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Hourglass/Internal/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Time
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Time/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Time/*.dyn_hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Hourglass/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Hourglass/Internal/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Time/*.p_hi
%endif
