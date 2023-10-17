import { UserContext } from "@/components/contexts";
import React from "react";

export default function RoleBadges() {
  const userContext = React.useContext(UserContext);

  if (userContext == null) {
    return <></>;
  } else {
    return (
      <>
        {userContext.verified ? (
          <span className="badge text-bg-secondary me-1">
            <i className="bi-check me-1" />
            Verified
          </span>
        ) : (
          <span className="badge text-bg-warning me-1">
            <i className="bi-x me-1" />
            Unverified
          </span>
        )}
        {userContext.admin ? (
          <span className="badge text-bg-primary me-1">
            <i className="bi-shield-shaded me-1" />
            Administrator
          </span>
        ) : undefined}
      </>
    );
  }
}
