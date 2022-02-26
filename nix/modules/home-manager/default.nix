{ config, lib, pkgs, ... }:

with lib;
let
  cfg = config.programs.sab;
in
{
  meta.maintainers = [ wolfangaukang ];

  options.programs.sab = {
    enable = mkEnableOption "Enables stream-alert-bot on your system";
    bots = mkOption {
      type = with types;
        let
          botSetup = submodule ({ config, name, ...}: {
            options = {
              #name = mkOption {
              #  type = strMatching "[a-zA-Z0-9-]{1,20}";
              #  description = ''
              #    Name of the bot. This is how the systemd file will be named.
              #  '';
              #  default = null;
              #};
              settingsPath = mkOption {
                type = path;
                description = ''
                  Path to the bot settings.
                '';
                default = null;
              };

              consumerType = mkOption {
                type = strMatching "(twitch|trovo)";
                description = ''
                  Consumer to check. Must be twitch or trovo.
                '';
                default = null;
              };

              # WIP
              #publisherType = mkOption {
              #  type = strMatching "";
              #  description = ''
              #    Publishers to notify. Must be one of twitter (default).
              #  '';
              #};
            };
          });
        in attrsOf botSetup;
      default = [ ]; 
      example = literalExpression ''
          [
            { id = "cjpalhdlnbpafiamejdnhcphjbkeiagm"; } # ublock origin
            {
              id = "dcpihecpambacapedldabdbpakmachpb";
              updateUrl = "https://raw.githubusercontent.com/iamadamdev/bypass-paywalls-chrome/master/updates.xml";
            }
            {
              id = "aaaaaaaaaabbbbbbbbbbcccccccccc";
              crxPath = "/home/share/extension.crx";
              version = "1.0";
            }
          ]
      '';
      description = "Bots configuration.";
    };

  };
  
  config = mkIf cfg.enable {
    home.packages = with pkgs; [ stream-alert-bot ]; 
    systemd.user.services = (flip mapAttrs' cfg.bots (name: bot: nameValuePair "sab-${toString name}" {
      Unit = {
        Description = "Alerts when a streamer on ${bot.consumerType} is live";
        After = [ "network.target" ];
      };
      Service = {
        ExecStart = "${pkgs.stream-alert-bot}/bin/stream_alert_bot -d ${bot.settingsPath} ${bot.consumerType}";
        Restart = "on-failure";
      };
      Install = {
        WantedBy = [ "default.target" ];
      };
    }));
  }; 
}
