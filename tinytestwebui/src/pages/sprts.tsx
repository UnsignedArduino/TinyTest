import Layout from "@/components/Layout";
import getAppProps, { AppProps } from "@/components/WithAppProps";

const pageName = "SPRTs";

export default function SPRTs({ appProps }: { appProps: AppProps }) {
  return (
    <Layout title={pageName} currentPage={pageName} appProps={appProps}>
      <>
        <h1>SPRTs</h1>
        <p>
          Below you can view all queued, running, and completed SPRTs for
          TinyChess.
        </p>
      </>
    </Layout>
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
