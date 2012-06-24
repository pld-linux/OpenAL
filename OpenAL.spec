#
# Conditional build:
# _without_alsa		- without ALSA support
# _without_doc		- don't build HTML documentation (from SGML source)
# _with_mmx		- use MMX (won't run on non-MMX CPU)
#
%ifarch athlon
%define		_with_mmx	1
%endif
%ifnarch i586 i686 athlon
%define		_with_mmx	0
%endif
Summary:	Open Audio Library
Summary(pl):	Otwarta Biblioteka D�wi�ku
Name:		OpenAL
Version:	0.0.6
%define	snap	20030218
Release:	1.%{snap}.1
License:	LGPL
Group:		Libraries
# from CVS :pserver:guest@opensource.creative.com:/usr/local/cvs-repository /openal
# (without all Win and Mac stuff and demos)
Source0:	%{name}-linuxonly-%{snap}.tar.bz2
Patch0:		%{name}-prefix.patch
Patch1:		%{name}-acfix.patch
Patch2:		%{name}-info.patch
URL:		http://www.openal.com/
BuildRequires:	SDL-devel
%{!?_without_alsa:BuildRequires:	alsa-lib-devel}
BuildRequires:	autoconf
BuildRequires:	automake
%{!?_without_doc:BuildRequires:	docbook-utils}
%{!?_without_doc:BuildRequires:	gnome-doc-tools}
BuildRequires:	libvorbis-devel
%{?_with_mmx:BuildRequires:	nasm}
BuildRequires:	smpeg-devel
BuildRequires:	texinfo
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix		/usr/X11R6

%description
OpenAL, the Open Audio Library, is a joint effort to create an open,
vendor-neutral, cross-platform API for interactive, primarily
spatialized audio. OpenAL's primary audience are application
developers and desktop users that rely on portable standards like
OpenGL, for games and other multimedia applications. OpenAL is already
supported by a number of hardware vendors and developers.

%description -l pl
OpenAL, otwarta biblioteka d�wi�ku, to po��czony wysi�ek w celu
stworzenia otwartego, niezale�nego od producent�w, miedzyplatformowego
interfejsu projektowania aplikacji w cz�ci obs�ugi d�wi�ku.
Biblioteka adresowana jest do tw�rc�w aplikacji i u�ytkownik�w,
kt�rzy wybieraj� przeno�ne standardy, jak OpenGL, w grach i
aplikacjach multimedialnych. OpenAL posiada ju� wsparcie wielu
dostarczycieli sprz�tu i programist�w.

%package devel
Summary:	Headers for OpenAL
Summary(pl):	Pliki nag��wkowe do OpenAL
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
Header files for OpenAL-based programs.

%description devel -l pl
Pliki nag��wkowe potrzebne przy budowaniu program�w opartych na
OpenAL.

%package static
Summary:	OpenAL static library
Summary(pl):	Statyczna biblioteka OpenAL
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
OpenAL static library.

%description static -l pl
Biblioteka OpenAL do statycznego linkowania.

%prep
%setup -q -n openal
%patch0 -p1
%patch1 -p1
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
