cask "warp-custom" do
  version "0.0.11"
  sha256 "ee42c80467575b2cd4b14f7a6c93dc66707db731700f762148abdd51388b0438"

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
