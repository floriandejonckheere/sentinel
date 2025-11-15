import { ShieldCheckIcon, CogIcon, BriefcaseIcon, ClipboardDocumentCheckIcon, UserGroupIcon } from '@heroicons/react/24/outline'

export const roles = [
  { id: 'executive', name: 'Executive', description: 'Executive', icon: BriefcaseIcon, color: 'gray' },
  { id: 'security', name: 'Security', description: 'Security', icon: ShieldCheckIcon, color: 'red' },
  { id: 'compliance', name: 'Compliance', description: 'Compliance', icon: ClipboardDocumentCheckIcon, color: 'blue' },
  { id: 'technical', name: 'Technical', description: 'Technical', icon: CogIcon, color: 'yellow' },
  { id: 'global', name: 'Global', description: 'I manage all aspects of security', icon: UserGroupIcon, color: 'purple' },
]
