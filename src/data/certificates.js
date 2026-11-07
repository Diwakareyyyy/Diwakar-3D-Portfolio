/**
 * Certificates Data Configuration
 * ---------------------------------------------------------------------------
 * Re-exports the centralized credentials repository from portfolio-data.js.
 * All updates should be made directly in `src/data/portfolio-data.js`.
 */

import { CERTIFICATES as CENTRAL_CERTIFICATES } from './portfolio-data.js';

export const CERTIFICATES = CENTRAL_CERTIFICATES;
