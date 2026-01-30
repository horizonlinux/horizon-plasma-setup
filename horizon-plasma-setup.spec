%global qt6_minver 6.6.0
%global kf6_minver 6.5.0

%global commit 9ee33221806c9e1807c421a5a88a01475afed6c5
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20251208

%global orgname org.kde.plasmasetup

# https://docs.fedoraproject.org/en-US/packaging-guidelines/#_compiler_flags
%global _hardened_build 1

Name:           horizon-plasma-setup
Version:        0.1.0~%{date}git%{shortcommit}
Release:        2%{?dist}
Summary:        Initial setup for systems using KDE Plasma
License:        (GPL-2.0-or-later or GPL-3.0-or-later) and GPL-2.0-or-later and GPL-3.0-or-later and (LGPL-2.0-or-later or LGPL-3.0-or-later) and (LGPL-2.1-or-later or LGPL-3.0-or-later) and LGPL-2.1-or-later and BSD-2-Clause and CC0-1.0
URL:            https://invent.kde.org/plasma/plasma-setup
Source:         %{url}/-/archive/%{commit}/plasma-setup-%{shortcommit}.tar.bz2

# Backported changes

# Proposed changes

# Downstream only changes
Patch1001:      plasma-setup-load-horizon-wallpaper.patch
Patch1002:      plasma-setup-select-horizon-lookandfeel.patch

BuildRequires:  cmake(Qt6Core) >= %{qt6_minver}
BuildRequires:  cmake(Qt6Gui) >= %{qt6_minver}
BuildRequires:  cmake(Qt6Qml) >= %{qt6_minver}
BuildRequires:  cmake(Qt6QuickControls2) >= %{qt6_minver}
BuildRequires:  cmake(Qt6Svg) >= %{qt6_minver}
BuildRequires:  cmake(Qt6Widgets) >= %{qt6_minver}
BuildRequires:  cmake(Qt6DBus) >= %{qt6_minver}
BuildRequires:  cmake(KF6I18n) >= %{kf6_minver}
BuildRequires:  cmake(KF6Package) >= %{kf6_minver}
BuildRequires:  cmake(KF6Auth) >= %{kf6_minver}
BuildRequires:  cmake(KF6CoreAddons) >= %{kf6_minver}
BuildRequires:  cmake(KF6Config) >= %{kf6_minver}
BuildRequires:  cmake(KF6Screen)
BuildRequires:  cmake(LibKWorkspace)
BuildRequires:  cracklib-devel
BuildRequires:  extra-cmake-modules >= %{kf6_minver}
BuildRequires:  gcc-c++
BuildRequires:  git-core
BuildRequires:  systemd-rpm-macros
BuildRequires:  kf6-rpm-macros
BuildRequires:  libappstream-glib
BuildRequires:  qt6qml(org.kde.plasma.private.kcm_keyboard)

Requires:       qt6qml(org.kde.plasma.private.kcm_keyboard)

Requires:       dbus-common
Requires:       kf6-filesystem
Requires:       kf6-kauth

Requires:       horizon-themes >= 1.0-1

# Renamed from KDE Initial System Setup / kiss
Obsoletes:      kiss < %{version}-%{release}
Provides:       kiss = %{version}-%{release}
Provides:       kiss%{?_isa} = %{version}-%{release}

# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch:    %{ix86}

# Do not check .so files in an application-specific library directory
%global __provides_exclude_from ^%{_kf6_qmldir}/org/kde/plasmasetup/.*\\.so.*$


%description
%{summary}.


%prep
%autosetup -n plasma-setup-%{commit} -S git_am


%build
%cmake_kf6
%cmake_build


%install
%cmake_install

%find_lang %{orgname} --all-name
rm -fv %{buildroot}%{_kf6_libdir}/libcomponentspluginplugin.a


%preun
%systemd_preun plasma-setup.service


%post
%systemd_post plasma-setup.service


%postun
%systemd_postun plasma-setup.service


%files -f %{orgname}.lang
%license LICENSES/*
%config(noreplace) %{_sysconfdir}/xdg/plasmasetuprc
%{_libexecdir}/plasma-setup*
%{_kf6_libexecdir}/kauth/plasma-setup*
%{_kf6_qmldir}/org/kde/plasmasetup/
%{_kf6_plugindir}/packagestructure/plasmasetup.so
%{_kf6_datadir}/plasma/packages/%{orgname}.*/
%license %{_kf6_datadir}/plasma/packages/%{orgname}.finished/contents/ui/konqi-calling.png.license
%{_unitdir}/plasma-setup*
%{_sysusersdir}/plasma-setup*
%{_tmpfilesdir}/plasma-setup*
%{_datadir}/dbus-1/*/%{orgname}.*
%{_datadir}/polkit-1/actions/%{orgname}.*
%{_datadir}/polkit-1/rules.d/plasma-setup*
%{_datadir}/qlogging-categories6/plasmasetup.categories
%{_datadir}/plasma-setup/


%changelog
* Thu Jan 29 2026 Marcel Mrówka <micro.mail88@gmail.com>
- Create package, based of plasma-setup
