import { UserContext } from "@/components/contexts";
import { copyTextToClipboard } from "@/scripts/Utils/Clipboard";
import { NotificationType, notify } from "@/components/Notifications";
import React from "react";

export default function APITokenSetting() {
  const userContext = React.useContext(UserContext);
  const [hideToken, setHideToken] = React.useState(true);
  const [regenerating, setRegenerating] = React.useState(false);

  return (
    <div>
      <h2>API token</h2>
      <p>
        This API token is used for your TinyTest clients, allowing them to
        authenticate with the TinyTest server. Keep this safe like a password!
      </p>
      {userContext ? (
        <div className="input-group mb-3">
          <span className="input-group-text">API token</span>
          <input
            type={hideToken ? "password" : "text"}
            className="form-control"
            readOnly
            defaultValue={userContext.apiToken}
            disabled={regenerating}
          />
          <button
            className="btn btn-outline-secondary"
            type="button"
            disabled={regenerating}
            onClick={() => {
              setHideToken(!hideToken);
            }}
          >
            {hideToken ? "Show" : "Hide"}
          </button>
          <button
            className="btn btn-outline-secondary"
            type="button"
            disabled={regenerating}
            onClick={() => {
              if (copyTextToClipboard(userContext.apiToken)) {
                notify(
                  "Successfully copied to clipboard!",
                  NotificationType.Success,
                );
              } else {
                notify("Failed to copy to clipboard!", NotificationType.Error);
              }
            }}
          >
            Copy to clipboard
          </button>
        </div>
      ) : (
        <p>
          There was an error fetching the API token - try regenerating the API
          token!
        </p>
      )}
      <p>
        In case your API token is compromised, you can generate a new one here.
        This will invalidate all existing API tokens, including ones used by
        TinyTest clients. (Make sure to update them!) This will also refresh the
        page.
      </p>
      <button
        type="button"
        className="btn btn-danger"
        disabled={regenerating}
        onClick={() => {
          setRegenerating(true);
          setHideToken(true);
          fetch("/api/auth/regenerate-api-token").then((response) => {
            if (response.status === 200) {
              notify(
                "Successfully regenerated API token, reloading page!",
                NotificationType.Success,
              );
            } else {
              notify(
                "Failed to regenerate API token, reloading page!",
                NotificationType.Error,
              );
            }
            setTimeout(() => {
              window.location.reload();
            }, 5000);
          });
        }}
      >
        Regenerate API token
      </button>
    </div>
  );
}
