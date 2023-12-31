import Layout from "@/components/Layout";
import OpeningBookTable from "@/components/OpeningBookTable/OpeningBookTable";
import getAppProps, { AppProps } from "@/components/WithAppProps";
import React from "react";

const pageName = "Opening books";

export default function OpeningBooks({ appProps }: { appProps: AppProps }) {
  return (
    <Layout title={pageName} currentPage={pageName} appProps={appProps}>
      <>
        <h1>Opening books</h1>
        <p>
          You can view opening books that can be used in SPRTs in the table
          below!
        </p>
        <div className="alert alert-info" role="alert">
          Please be patient when downloading books!
        </div>
        <OpeningBookTable />
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
