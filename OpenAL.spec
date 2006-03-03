#
# Conditional build:
# TODO:
# - Build stops at:
# arch/i386/x86_floatmul.c:86:74: warning: use of C99 long long integer constant
# arch/i386/x86_floatmul.c:89:74: warning: use of C99 long long integer constant
# arch/i386/x86_floatmul.c: In function `_alFloatMul':
#arch/i386/x86_floatmul.c:86: internal compiler error: in ix86_expand_binop_builtin, at config/i386/i386.c:13246
# Please submit a full bug report,
#
# - autoconf provides undefined macro....

%bcond_without	alsa	# without ALSA support
%bcond_with	arts	# with aRts support
%bcond_without	doc	# don't build HTML documentation (from SGML source)
%bcond_without	esd	# without esd support
%bcond_with	mmx	# use MMX (makes sense on i[56]86 with MMX; won't run on non-MMX CPU)

Summary:	Open Audio Library
Summary(pl):	Otwarta Biblioteka D�wi�ku
Name:		OpenAL
Version:	0.0.8
Release:	0.1
License:	LGPL
Group:		Libraries
Source0:	http://www.openal.org/openal_webstf/downloads/openal-%{version}.tar.gz
# Source0-md5:	641cf53761f35ee979f3e888614797a0
#Patch0:		%{name}-prefix.patch
#Patch1:		%{name}-info.patch
URL:		http://www.openal.org/
BuildRequires:	SDL-devel
%{?with_alsa:BuildRequires:	alsa-lib-devel}
%{?with_arts:BuildRequires:	artsc-devel}
BuildRequires:	autoconf
BuildRequires:	automake
%{?with_doc:BuildRequires:	docbook-utils}
%{?with_esd:BuildRequires:	esound-devel}
%{?with_doc:BuildRequires:	gnome-doc-tools}
BuildRequires:	libvorbis-devel
%{?with_mmx:BuildRequires:	nasm}
BuildRequires:	smpeg-devel
BuildRequires:	texinfo
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
OpenAL, the Open Audio Library, is a joint effort to create an open,
vendor-neutral, cross-platform API for interactive, primarily
spatialized audio. OpenAL's primary audience are application
developers and desktop users that rely on portable standards like
OpenGL, for games and other multimedia applications. OpenAL is already
supported by a number of hardware vendors and developers.

%description -l pl
OpenAL, otwarta biblioteka d�wi�ku, to po��czony wysi�ek w celu
stworzenia otwartego, niezale�nego od producent�w, mi�dzyplatformowego
interfejsu projektowania aplikacji w cz�ci obs�ugi d�wi�ku.
Biblioteka adresowana jest do tw�rc�w aplikacji i u�ytkownik�w,
kt�rzy wybieraj� przeno�ne standardy, jak OpenGL, w grach i
aplikacjach multimedialnych. OpenAL posiada ju� wsparcie wielu
dostarczycieli sprz�tu i programist�w.

%package devel
Summary:	Headers for OpenAL
Summary(pl):	Pliki nag��wkowe do OpenAL
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for OpenAL-based programs.

%description devel -l pl
Pliki nag��wkowe potrzebne przy budowaniu program�w opartych na
OpenAL.

%package static
Summary:	OpenAL static library
Summary(pl):	Statyczna biblioteka OpenAL
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
OpenAL static library.

%description static -l pl
Biblioteka OpenAL do konsolidacji statycznej.

%prep
%setup -q -n openal-%{version}
#%patch0 -p1
#%patch1 -p1

%build
cp -f /usr/share/automake/config.sub .
#%{__aclocal}
#%{__autoconf}
#%{__autoheader}
%configure \
	%{?with_alsa:--enable-alsa --enable-alsa-dlopen} \
	%{?with_arts:--enable-arts --enable-arts-dlopen} \
	%{?with_esd:--enable-esd --enable-esd-dlopen} \
	--enable-sdl \
	--enable-vorbis \
	--enable-smpeg \
	--enable-capture \
	--with-gcc=%{__cc}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_infodir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post devel
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%postun	devel
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%files
%defattr(644,root,root,755)
%doc ChangeLog NOTES TODO
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*-config
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/*.la
%{_pkgconfigdir}/*
%{_includedir}/AL

%files static
%defattr(644,root,root,755)
%{_libdir}/*.a
