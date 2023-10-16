import { useSession } from "next-auth/react";

export default function Profile() {
  const { data: session, status } = useSession();
  if (status === "loading") {
    return (
      <>
        <button
          type="button"
          className="btn btn-secondary"
          data-bs-target="#profileOffcanvas"
          data-bs-toggle="offcanvas"
          aria-controls="profileOffcanvas"
          // disabled={true}
        >
          <p className="placeholder-glow m-0 p-0">
            <span className="placeholder" style={{ width: "3em" }} />
          </p>
        </button>
      </>
    );
  } else if (session) {
    return (
      <>
        <button
          type="button"
          className="btn p-0"
          data-bs-target="#profileOffcanvas"
          data-bs-toggle="offcanvas"
          aria-controls="profileOffcanvas"
        >
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img
            src={session.user!.image!}
            alt={`Profile picture of ${session.user!.name}`}
            style={{
              width: "2em",
              height: "2em",
              objectFit: "contain",
              borderRadius: "50%",
            }}
          />
        </button>
      </>
    );
  } else {
    return (
      <>
        <button
          type="button"
          className="btn btn-secondary"
          data-bs-target="#profileOffcanvas"
          data-bs-toggle="offcanvas"
          aria-controls="profileOffcanvas"
        >
          Sign in
        </button>
      </>
    );
  }
}
