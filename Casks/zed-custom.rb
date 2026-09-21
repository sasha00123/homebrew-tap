cask "zed-custom" do
  version "0.0.14"
  sha256 "65250100132c08135fec7bfe9fcdfa13543b7305c108d6fbb1bc6313eaca0c82"

  url "https://github.com/sasha00123/zed/releases/download/personal-v#{version}/zed-custom-#{version}-macos-arm64.zip"
  name "Zed Custom"
  desc "Unofficial personal build of Zed"
  homepage "https://github.com/sasha00123/zed"

  depends_on arch: :arm64
  depends_on formula: "git"
  depends_on macos: :ventura

  app "Zed Custom.app"

  caveats <<~EOS
    This personal build is ad-hoc signed, not Apple-notarized.
    Update via this tap. Upstream self-updating is disabled.
    Source and licenses: https://github.com/sasha00123/zed/releases/tag/personal-v#{version}
  EOS
end
