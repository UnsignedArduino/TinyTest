import { UserContext } from "@/components/contexts";
import { NotificationType, notify } from "@/components/Notifications";
import React from "react";
import CopyToClipboardButton from "@/components/Buttons/CopyToClipboard";

export default function APITokenSetting() {
  const userContext = React.useContext(UserContext);
  const [hideToken, setHideToken] = React.useState(true);
  const [regenerating, setRegenerating] = React.useState(false);
  const [regenAsReload, setRegenAsReload] = React.useState(false);

  return (
    <div>
      <h2>API token</h2>
      <p>
        This API token is used by your TinyTest clients, (allowing them to
        authenticate with the TinyTest server) and the web UI. Keep this safe
        like a password!
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
            title={hideToken ? "Hide token" : "Show token"}
          >
            {hideToken ? (
              <i className="bi-eye" />
            ) : (
              <i className="bi-eye-slash" />
            )}
          </button>
          <CopyToClipboardButton
            text={userContext.apiToken}
            disabled={regenerating}
          />
        </div>
      ) : (
        <p>
          There was an error fetching the API token - try regenerating the API
          token!
        </p>
      )}
      <p>
        In case your API token is compromised, you can generate a new one here.
        This will invalidate the current API token, including ones used by
        TinyTest clients. (Make sure to update them!) This will also prompt a
        page reload in order to refresh the web UI.
      </p>
      <button
        type="button"
        className={`btn btn-${regenAsReload ? "success" : "danger"}`}
        disabled={regenerating && !regenAsReload}
        onClick={() => {
          if (regenAsReload) {
            window.location.reload();
          }
          setRegenerating(true);
          setHideToken(true);
          fetch("/api/auth/regenerate-api-token").then((response) => {
            if (response.status === 200) {
              notify(
                "Successfully regenerated API token, reloading page!",
                NotificationType.Success,
              );
              setRegenAsReload(true);
            } else {
              notify(
                "Failed to regenerate API token, reloading page!",
                NotificationType.Error,
              );
              setRegenerating(false);
            }
          });
        }}
      >
        {regenAsReload ? (
          <>
            <i className="bi-check-lg me-2" /> Success - click to reload
          </>
        ) : (
          <>
            <i className="bi-arrow-repeat me-2" />
            Regenerate API token
          </>
        )}
      </button>
    </div>
  );
}
