#
# Conditional build:
%bcond_without	alsa	# without ALSA support
%bcond_with	arts	# with aRts support
%bcond_without	doc	# don't build HTML documentation (from SGML source)
%bcond_without	esd	# without esd support
%bcond_with	mmx	# use MMX (makes sense on i[56]86 with MMX; won't run on non-MMX CPU)
			# Currently broken.
#
# TODO:
# - remove zip BR?
#

%define	_branch	Linux_Spec1-0

Summary:	Open Audio Library
Summary(pl):	Otwarta Biblioteka D¼wiêku
Name:		OpenAL
Version:	0.0.8
%define	snap	20051015
Release:	0.%{snap}.1
License:	LGPL
Group:		Libraries
# from CVS :pserver:guest@opensource.creative.com:/usr/local/cvs-repository /openal
# (without all Win and Mac stuff and demos)
Source0:	%{name}-%{_branch}-%{snap}.tar.bz2
# Source0-md5:	013a571cf588bec1d3a5628b5ed527ea
Patch0:		%{name}-prefix.patch
Patch1:		%{name}-info.patch
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
BuildRequires:	zip
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
%setup -q -n %{name}-%{_branch}-%{snap}
%patch0 -p1
%patch1 -p1

cp CREDITS docs

%build
cd linux
cp -f /usr/share/automake/config.sub .
%{__aclocal}
%{__autoconf}
%{__autoheader}
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

cd ../docs/spec1-0
%{?with_doc:%{__make} full-html}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_infodir}

%{__make} -C linux install \
	DESTLIB='$(DESTDIR)%{_libdir}' \
	DESTDIR=$RPM_BUILD_ROOT

install linux/doc/openal.info $RPM_BUILD_ROOT%{_infodir}

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
%doc linux/{CREDITS,ChangeLog,NOTES,TODO}
%attr(755,root,root) %{_libdir}/lib*.so.*.*

%files devel
%defattr(644,root,root,755)
%doc linux/doc/LOKI* %{?with_doc:docs/spec1-0/oalspecs-full docs/spec1-1/OpenAL1-1Spec.pdf}
%attr(755,root,root) %{_libdir}/lib*.so
%attr(755,root,root) %{_bindir}/*-config
%{_pkgconfigdir}/*
%{_includedir}/AL
%{_infodir}/openal.info*

%files static
%defattr(644,root,root,755)
%{_libdir}/*.a
