async def notion(message, text, state, FSM, yes_no_kb):

    await message.answer(text=text, reply_markup=yes_no_kb)

    await state.set_state(FSM.is_train)