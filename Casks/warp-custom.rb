cask "warp-custom" do
  version "0.0.13"
  sha256 "f1fcdda0e3aa72fd3e87821cf6cad352d8ca3ae1361b48a31702c67a7b1a747e"

  url "https://github.com/sasha00123/warp/releases/download/personal-v#{version}/warp-custom-#{version}-macos-arm64.zip"
  name "Warp Custom"
  desc "Unofficial personal build of Warp"
  homepage "https://github.com/sasha00123/warp"

  depends_on arch: :arm64
  depends_on macos: :ventura

  app "Warp Custom.app"

  caveats <<~EOS
    This personal build is ad-hoc signed, not Apple-notarized.
    Update via this tap. Upstream self-updating is disabled.
    Source and licenses: https://github.com/sasha00123/warp/releases/tag/personal-v#{version}
  EOS
end
