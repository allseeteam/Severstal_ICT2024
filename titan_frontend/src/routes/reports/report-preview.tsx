import React from 'react';
import { useParams } from 'react-router-dom';

const ReportPreviewPage = () => {
  const params = useParams();
  console.log(params.reportId);
  return <div>ReportPreviewPage</div>;
};

export default ReportPreviewPage;
