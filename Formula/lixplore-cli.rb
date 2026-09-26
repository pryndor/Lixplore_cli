# To get sha256 hashes, run:
#   pip download --no-deps --no-binary :all: lixplore-cli==1.0.1 -d /tmp/hashes
#   pip download --no-deps --no-binary :all: biopython==1.84 -d /tmp/hashes
#   pip download --no-deps --no-binary :all: requests==2.32.3 -d /tmp/hashes
#   pip download --no-deps --no-binary :all: openpyxl==3.1.5 -d /tmp/hashes
#   sha256sum /tmp/hashes/*.tar.gz
# Then replace PLACEHOLDER below with the actual hashes.

class LixploreCli < Formula
  include Language::Python::Virtualenv

  desc "Academic Literature Search & Export CLI Tool"
  homepage "https://github.com/pryndor/Lixplore_cli"
  url "https://files.pythonhosted.org/packages/source/l/lixplore-cli/lixplore_cli-1.0.1.tar.gz"
  sha256 "PLACEHOLDER"
  license "MIT"

  depends_on "python@3.12"

  resource "biopython" do
    url "https://files.pythonhosted.org/packages/source/b/biopython/biopython-1.84.tar.gz"
    sha256 "PLACEHOLDER"
  end

  resource "requests" do
    url "https://files.pythonhosted.org/packages/source/r/requests/requests-2.32.3.tar.gz"
    sha256 "PLACEHOLDER"
  end

  resource "openpyxl" do
    url "https://files.pythonhosted.org/packages/source/o/openpyxl/openpyxl-3.1.5.tar.gz"
    sha256 "PLACEHOLDER"
  end

  def install
    virtualenv_install_with_resources
  end

  test do
    assert_match "lixplore", shell_output("#{bin}/lixplore --version 2>&1", 0)
  end
end
