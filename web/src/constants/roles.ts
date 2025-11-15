import { ShieldCheckIcon, CogIcon, BriefcaseIcon, ClipboardDocumentCheckIcon } from '@heroicons/react/24/outline'

export const roles = [
  { id: 'executive', label: 'Executive', icon: BriefcaseIcon, color: 'gray' },
  { id: 'security', label: 'Security', icon: ShieldCheckIcon, color: 'red' },
  { id: 'compliance', label: 'Compliance', icon: ClipboardDocumentCheckIcon, color: 'blue' },
  { id: 'technical', label: 'Technical', icon: CogIcon, color: 'yellow' },
]
