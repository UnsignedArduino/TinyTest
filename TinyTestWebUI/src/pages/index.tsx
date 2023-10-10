import Layout from "@/components/Layout";
import { promises as fs } from "fs";
import getAppProps, { AppProps } from "@/components/WithAppProps";
import generateSiteWebmanifest from "@/scripts/Utils/SiteWebmanifest";

const pageName = "Home";

export default function Home({ appProps }: { appProps: AppProps }) {
  return (
    <Layout title={pageName} currentPage={pageName} appProps={appProps}>
      <>
        <h1>Welcome to TinyTest</h1>
        TinyTest is the distributed testing program for{" "}
        <a
          href="https://github.com/Bobingstern/TinyChess"
          target="_blank"
          rel="noopener noreferrer"
        >
          TinyChess
        </a>
        , a UCI chess engine designed to run with low RAM.
      </>
    </Layout>
  );
}

export async function getStaticProps(): Promise<{
  props: { appProps: AppProps };
}> {
  await fs.writeFile(
    "./public/site.webmanifest",
    await generateSiteWebmanifest(),
  );

  return {
    props: {
      appProps: await getAppProps(),
    },
  };
}
