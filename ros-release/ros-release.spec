Name:           ros-release
Version:        10
Release:        %autorelease
Summary:        Packages for ROS repository configuration
BuildArch: noarch
License: ASL 2.0
URL: https://github.com/ros-infrastructure/ros-archive-keyring
Source0: README.md
Source1: copyright
 
# keys
Source10:       https://download.fedoraproject.org/pub/epel/RPM-GPG-KEY-EPEL-%{version}
 
# repo configs
Source20:       ros2.repo
Source21:       ros2-testing.repo
Source22:       ros.repo
Source23:       ros-testing.repo

 
# This should only be installed on Enterprise Linux with the same major version
Requires:       (redhat-release >= %{version} with redhat-release < %[%{version} + 1])
# crb needs config-manager to run
# But only recommend it, incase people do not need crb
Recommends:     dnf-command(config-manager)
# SELinux policy modules related to EPEL
Recommends:     (selinux-policy-epel if selinux-policy)
 
%description
This package contains the ROS and ROS 2 repository
configuration and GPG key.
 
%prep
%setup -q -c -T
 
%install
# keys
install -Dp -m 0644 -t %{buildroot}%{_sysconfdir}/pki/rpm-gpg %{S:10}
 
# repo configs
install -Dp -m 0644 -t %{buildroot}%{_sysconfdir}/yum.repos.d %{S:20} %{S:21}
 
# preset policy
install -Dp -m 0644 -t %{buildroot}%{_prefix}/lib/systemd/system-preset %{S:30}

%package -n ros-release
Conflicts: ros-testing-release
%files
%config(noreplace) %{_sysconfdir}/yum.repos.d/ros.repo


%package -n ros-testing-release
Conflicts: ros-release
%files
%config(noreplace) %{_sysconfdir}/yum.repos.d/ros-testing.repo


%package -n ros2-release
Conflicts: ros2-testing-release
%files
%config(noreplace) %{_sysconfdir}/yum.repos.d/ros2.repo


%package -n ros2-testing-release
Conflicts: ros2-release
%files
%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-EPEL-%{version}
%config(noreplace) %{_sysconfdir}/yum.repos.d/ros2-testing.repo
 
 
%files
%license copyright
%doc README.md
 
 
%changelog
%autochangelog
