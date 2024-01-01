import accordion from './accordion/index.js'
import autocomplete from './autocomplete/index.js'
import avatar from './avatar/index.js'
import avatargroup from './avatargroup/index.js'
import badge from './badge/index.js'
import badgedirective from './badgedirective/index.js'
import button from './button/index.js'
import calendar from './calendar/index.js'
import card from './card/index.js'
import cascadeselect from './cascadeselect/index.js'
import checkbox from './checkbox/index.js'
import chip from './chip/index.js'
import chips from './chips/index.js'
import colorpicker from './colorpicker/index.js'
import contextmenu from './contextmenu/index.js'
import datatable from './datatable/index.js'
import dialog from './dialog/index.js'
import divider from './divider/index.js'
import dropdown from './dropdown/index.js'
import fieldset from './fieldset/index.js'
import global from './global.js'
import inlinemessage from './inlinemessage/index.js'
import inputgroup from './inputgroup/index.js'
import inputgroupaddon from './inputgroupaddon/index.js'
import inputmask from './inputmask/index.js'
import inputnumber from './inputnumber/index.js'
import inputswitch from './inputswitch/index.js'
import inputtext from './inputtext/index.js'
import knob from './knob/index.js'
import listbox from './listbox/index.js'
import menu from './menu/index.js'
import menubar from './menubar/index.js'
import message from './message/index.js'
import multiselect from './multiselect/index.js'
import overlaypanel from './overlaypanel/index.js'
import paginator from './paginator/index.js'
import panel from './panel/index.js'
import password from './password/index.js'
import progressbar from './progressbar/index.js'
import radiobutton from './radiobutton/index.js'
import rating from './rating/index.js'
import ripple from './ripple/index.js'
import selectbutton from './selectbutton/index.js'
import sidebar from './sidebar/index.js'
import skeleton from './skeleton/index.js'
import slider from './slider/index.js'
import splitbutton from './splitbutton/index.js'
import steps from './steps/index.js'
import tabview from './tabview/index.js'
import tag from './tag/index.js'
import textarea from './textarea/index.js'
import tieredmenu from './tieredmenu/index.js'
import toast from './toast/index.js'
import togglebutton from './togglebutton/index.js'
import tooltip from './tooltip/index.js'
import tree from './tree/index.js'
import treeselect from './treeselect/index.js'
import tristatecheckbox from './tristatecheckbox/index.js'

export default {
  global,
  directives: {
    badge: badgedirective,
    ripple,
    tooltip
  },

  //forms
  autocomplete,
  dropdown,
  inputnumber,
  inputtext,
  calendar,
  checkbox,
  radiobutton,
  inputswitch,
  selectbutton,
  slider,
  chips,
  rating,
  multiselect,
  togglebutton,
  cascadeselect,
  listbox,
  colorpicker,
  inputgroup,
  inputgroupaddon,
  inputmask,
  knob,
  treeselect,
  tristatecheckbox,
  textarea,
  password,

  //buttons
  button,
  splitbutton,

  //data
  paginator,
  datatable,
  tree,

  //panels
  accordion,
  panel,
  fieldset,
  card,
  tabview,
  divider,

  //menu
  contextmenu,
  menu,
  menubar,
  steps,
  tieredmenu,

  //overlays
  dialog,
  overlaypanel,
  sidebar,

  //messages
  message,
  inlinemessage,
  toast,

  //misc
  badge,
  avatar,
  avatargroup,
  tag,
  chip,
  progressbar,
  skeleton
}
