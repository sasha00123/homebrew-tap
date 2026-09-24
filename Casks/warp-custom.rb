cask "warp-custom" do
  version "0.0.12"
  sha256 "f06aec40824d2b5ecb7308175106607f2c99f8974f90e71f5534f15c06a48bb2"

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
