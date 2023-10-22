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
        "ngrok-skip-browser-warning": "pls",
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
  body: any = null,
  apiKey: string | null = null,
) {
  const url = process.env.NEXT_PUBLIC_API_SERVER_URL + path;
  console.log(
    `Making ${apiKey !== null ? "authenticated " : ""}API request to ${url}`,
  );
  const headers = new Headers({
    "Content-Type": "application/json",
    "ngrok-skip-browser-warning": "pls",
  });
  if (apiKey !== null) {
    headers.set("x-api-token", apiKey);
  }
  const response = await fetch(
    new Request(url, {
      method: method,
      headers: headers,
      body: body,
    }),
  );
  if (response.status === 500) {
    throw new Error("Internal server error when making API call");
  }
  return response;
}

export async function FormDataCallDirectAsUser(
  path: string,
  method: string = "GET",
  formData: FormData,
  apiKey: string | null = null,
) {
  const url = process.env.NEXT_PUBLIC_API_SERVER_URL + path;
  console.log(
    `Making ${apiKey !== null ? "authenticated " : ""}API request to ${url}`,
  );
  const headers = new Headers({
    "ngrok-skip-browser-warning": "pls",
  });
  if (apiKey !== null) {
    headers.set("x-api-token", apiKey);
  }
  const response = await fetch(
    new Request(url, {
      method: method,
      headers: headers,
      body: formData,
    }),
  );
  if (response.status === 500) {
    throw new Error("Internal server error when making API call");
  }
  return response;
}
