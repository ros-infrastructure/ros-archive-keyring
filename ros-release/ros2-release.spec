Name:           ros2-release
Version:        1.0.0
Summary:        Packages for ROS 2 main repository configuration
Release: 1%{?dist}%{?release_suffix}
BuildArch: noarch
License: ASL 2.0
URL: https://github.com/ros-infrastructure/ros-apt-source
Source0: README.md
Source1: copyright
Requires:  dnf-command(config-manager)
Requires:  epel-release
Conflicts: ros2-testing-release

Source10:       ros2-key.gpg
Source20:       ros2.repo


 
%description
This package contains the ROS 2 repository configuration and GPG key.
 
%prep
%setup -q -c -T
cp -a %{SOURCE0} %{SOURCE1} .
 
%install
install -Dp -m 0644 -t %{buildroot}%{_sysconfdir}/pki/rpm-gpg %{S:10}
install -Dp -m 0644 -t %{buildroot}%{_sysconfdir}/yum.repos.d %{S:20}

%build 

%files
%license copyright
%doc README.md
%{_sysconfdir}/pki/rpm-gpg/ros2-key.gpg
%config(noreplace) %{_sysconfdir}/yum.repos.d/ros2.repo


 
 
%changelog
* Wed Apr 30 2025 Clara Berendsen - 1.0.0-1
- Initial package creation.
