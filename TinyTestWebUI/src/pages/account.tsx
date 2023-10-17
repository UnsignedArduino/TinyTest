import Layout from "@/components/Layout";
import getAppProps, { AppProps } from "@/components/WithAppProps";
import React from "react";
import RequireSignedIn from "@/components/AccessManagement/RequireSignedIn";
import { useSession } from "next-auth/react";
import APITokenSetting from "@/components/Settings/APITokenSetting";
import RoleBadges from "@/components/Settings/RoleBadges";
import { UserContext } from "@/components/contexts";

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
  const userContext = React.useContext(UserContext);

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
        <br />
        <div className="mt-1">
          <RoleBadges />
        </div>
        {userContext != null && !userContext.verified ? (
          <div className="alert alert-warning mt-2" role="alert">
            You are currently unverified, please wait for an administrator to
            manually verify you!
          </div>
        ) : undefined}
      </p>
      <APITokenSetting />
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
