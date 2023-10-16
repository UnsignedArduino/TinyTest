import Layout from "@/components/Layout";
import getAppProps, { AppProps } from "@/components/WithAppProps";
import React from "react";
import RequireSignedIn from "@/components/AccessManagement/RequireSignedIn";
import { UserAPITokenContext } from "@/components/contexts";
import { useSession } from "next-auth/react";
import { copyTextToClipboard } from "@/scripts/Utils/Clipboard";
import { NotificationType, notify } from "@/components/Notifications";

const pageName = "Account";

export default function Account({ appProps }: { appProps: AppProps }) {
  return (
    <Layout title={pageName} currentPage={pageName} appProps={appProps}>
      <>
        <h1>Account</h1>
        <RequireSignedIn>
          <AccountSignedIn />
        </RequireSignedIn>
      </>
    </Layout>
  );
}

function AccountSignedIn() {
  const { data: session } = useSession();

  return (
    <div>
      <p>
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img
          src={session!.user!.image!}
          alt={`Profile picture of ${session!.user!.name}`}
          style={{
            width: "1.5em",
            height: "1.5em",
            objectFit: "contain",
            borderRadius: "50%",
          }}
        />{" "}
        <span>Signed in as {session!.user!.name}.</span>
      </p>
      <APITokenSetting />
    </div>
  );
}

function APITokenSetting() {
  const apiToken = React.useContext(UserAPITokenContext);
  const [hideToken, setHideToken] = React.useState(true);
  const [regenerating, setRegenerating] = React.useState(false);

  return (
    <div>
      <h2>API token</h2>
      <p>
        This API token is used for your TinyTest clients, allowing them to
        authenticate with the TinyTest server. Keep this safe like a password!
      </p>
      {apiToken ? (
        <div className="input-group mb-3">
          <span className="input-group-text">API token</span>
          <input
            type={hideToken ? "password" : "text"}
            className="form-control"
            readOnly
            defaultValue={apiToken}
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
              if (copyTextToClipboard(apiToken)) {
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
              setRegenerating(false);
            }
            window.location.reload();
          });
        }}
      >
        Regenerate API token
      </button>
    </div>
  );
}

export async function getStaticProps(): Promise<{
  props: { appProps: AppProps };
}> {
  return {
    props: {
      appProps: await getAppProps(),
    },
  };
}
