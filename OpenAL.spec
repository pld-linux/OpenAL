#
# Conditional build:
# _without_alsa		- without ALSA support
# _without_doc		- don't build HTML documentation (from SGML source)
# _without_esd		- without esd support
# _with_mmx		- use MMX (makes sense on i[56]86 with MMX; won't run on non-MMX CPU)
#
# TODO:
# - remove zip bcond?
# - check %{name}-acfix.patch if it's still nedded, sorry
#   for the inconvenience, I'll do it if I can...
#
%ifarch athlon
%define		_with_mmx	1
%endif

%ifarch sparc
%define		_without_alsa	1
%endif


Summary:	Open Audio Library
Summary(pl):	Otwarta Biblioteka D¼wiêku
Name:		OpenAL
Version:	0.0.6
%define	snap	20030806
Release:	1.%{snap}.0.10
License:	LGPL
Group:		Libraries
# from CVS :pserver:guest@opensource.creative.com:/usr/local/cvs-repository /openal
# (without all Win and Mac stuff and demos)
Source0:	http://pb152.srem.sdi.tpnet.pl/pld/%{name}-linuxonly-%{snap}.tar.bz2
# Source0-md5:	4a5202f6cba291ae0a9af59410bdda88
Patch0:		%{name}-prefix.patch
Patch1:		%{name}-acfix.patch
Patch2:		%{name}-info.patch
URL:		http://www.openal.org/
BuildRequires:	SDL-devel
%{!?_without_alsa:BuildRequires:	alsa-lib-devel}
BuildRequires:	autoconf
BuildRequires:	automake
%{!?_without_doc:BuildRequires:	docbook-utils}
%{!?_without_esd:BuildRequires:	esound-devel}
%{!?_without_doc:BuildRequires:	gnome-doc-tools}
BuildRequires:	libvorbis-devel
%{?_with_mmx:BuildRequires:	nasm}
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
Requires:	%{name} = %{version}

%description devel
Header files for OpenAL-based programs.

%description devel -l pl
Pliki nag³ówkowe potrzebne przy budowaniu programów opartych na
OpenAL.

%package static
Summary:	OpenAL static library
Summary(pl):	Statyczna biblioteka OpenAL
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
OpenAL static library.

%description static -l pl
Biblioteka OpenAL do konsolidacji statycznej.

%prep
%setup -q -n openal
%patch0 -p1
#%%patch1 -p1
%patch2 -p1

echo 'AC_DEFUN([AC_HAS_MMX],[$%{?_with_mmx:1}%{!?_with_mmx:2}])' >> linux/acinclude.m4

%build
cd linux
%{__aclocal}
%{__autoconf}
%{__autoheader}
%configure \
	%{!?debug:--enable-optimization} \
	%{?_with_mmx:--enable-arch-asm} \
	%{!?_without_alsa:--enable-alsa} \
	%{!?_without_esd:--enable-esd} \
	--enable-sdl \
	--enable-vorbis \
	--enable-smpeg \
	--enable-capture \
	--with-gcc=%{__cc}

%{__make}

cd ../docs
%{!?_without_doc:%{__make} full-html}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_infodir}

cd linux
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install doc/openal.info $RPM_BUILD_ROOT%{_infodir}

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
%doc linux/doc/LOKI* %{!?_without_doc:docs/oalspecs-full}
%attr(755,root,root) %{_libdir}/lib*.so
%{_includedir}/AL
%{_infodir}/openal.info*

%files static
%defattr(644,root,root,755)
%attr(755,root,root)%{_libdir}/*.a
