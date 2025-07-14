import React, { FC } from 'react';

export const Spinner: FC = () => (
  <div className="flex justify-center items-center p-8">
    <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-500"></div>
  </div>
);
