#
# TODO:
# - Build stops at:
# arch/i386/x86_floatmul.c:86:74: warning: use of C99 long long integer constant
# arch/i386/x86_floatmul.c:89:74: warning: use of C99 long long integer constant
# arch/i386/x86_floatmul.c: In function `_alFloatMul':
#arch/i386/x86_floatmul.c:86: internal compiler error: in ix86_expand_binop_builtin, at config/i386/i386.c:13246
# Please submit a full bug report,
#
# - autoconf provides undefined macro....

# Conditional build:
#
%bcond_without	alsa	# without ALSA support
%bcond_with	arts	# with aRts support
%bcond_without	esd	# without esd support
%bcond_with	mmx	# use MMX (makes sense on i[56]86 with MMX; won't run on non-MMX CPU)

Summary:	Open Audio Library
Summary(pl):	Otwarta Biblioteka D¼wiêku
Name:		OpenAL
Version:	0.0.8
Release:	1
License:	LGPL
Group:		Libraries
Source0:	http://www.openal.org/openal_webstf/downloads/openal-%{version}.tar.gz
# Source0-md5:	641cf53761f35ee979f3e888614797a0
URL:		http://www.openal.org/
BuildRequires:	SDL-devel
%{?with_alsa:BuildRequires:	alsa-lib-devel}
%{?with_arts:BuildRequires:	artsc-devel}
%{?with_esd:BuildRequires:	esound-devel}
BuildRequires:	libvorbis-devel
%{?with_mmx:BuildRequires:	nasm}
BuildRequires:	smpeg-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
OpenAL, the Open Audio Library, is a joint effort to create an open,
vendor-neutral, cross-platform API for interactive, primarily
spatialized audio. OpenAL's primary audience are application
developers and desktop users that rely on portable standards like
OpenGL, for games and other multimedia applications. OpenAL is already
supported by a number of hardware vendors and developers.

%description -l pl
OpenAL, otwarta biblioteka d¼wiêku, to po³±czony wysi³ek w celu
stworzenia otwartego, niezale¿nego od producentów, miêdzyplatformowego
interfejsu projektowania aplikacji w czê¶ci obs³ugi d¼wiêku.
Biblioteka adresowana jest do twórców aplikacji i u¿ytkowników,
którzy wybieraj± przeno¶ne standardy, jak OpenGL, w grach i
aplikacjach multimedialnych. OpenAL posiada ju¿ wsparcie wielu
dostarczycieli sprzêtu i programistów.

%package devel
Summary:	Headers for OpenAL
Summary(pl):	Pliki nag³ówkowe do OpenAL
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for OpenAL-based programs.

%description devel -l pl
Pliki nag³ówkowe potrzebne przy budowaniu programów opartych na
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

%build
%configure \
	%{?with_alsa:--enable-alsa --enable-alsa-dlopen} \
	%{?with_arts:--enable-arts --enable-arts-dlopen} \
	%{?with_esd:--enable-esd --enable-esd-dlopen} \
	--enable-sdl --enable-sdl-dlopen \
	--enable-capture \
	--enable-linux \
	--enable-null \
	--enable-waveout \
	--enable-vorbis --enable-vorbis-dlopen \
	--enable-mp3 --enable-mp3-dlopen \
	--with-gcc=%{__cc}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

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
