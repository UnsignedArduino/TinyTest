export async function APICallAsSystem(
  path: string,
  method: string = "GET",
  body: string | undefined,
) {
  const url = (process.env.NEXT_PUBLIC_API_SERVER_URL as string) + path;
  console.log(`Making API request to ${url}`);
  const response = await fetch(
    new Request(url, {
      method: method,
      headers: {
        "Content-Type": "application/json",
        "X-API-token": process.env.SYSTEM_API_KEY as string,
      },
      body: body,
    }),
  );
  if (response.status === 500) {
    throw new Error("Internal server error when making API call");
  }
  return response;
}

export async function APICallDirectAsUser(
  path: string,
  method: string = "GET",
  body: string | undefined,
) {
  const url = process.env.NEXT_PUBLIC_API_SERVER_URL + path;
  console.log(`Making API request to ${url}`);
  const response = await fetch(
    new Request(url, {
      method: method,
      headers: {
        "Content-Type": "application/json",
      },
      body: body,
    }),
  );
  if (response.status === 500) {
    throw new Error("Internal server error when making API call");
  }
  return response;
}
